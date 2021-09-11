import json
import re
import base64
import jwt

from urllib.parse import unquote
from django.http  import JsonResponse
from django.db.models import Q, Count, Avg, Case, When
from django.http      import JsonResponse
from django.views     import View
from django.conf      import settings

from .models          import Product, Category, User, UserProductLike
from comments.models  import Comment
from .decorator       import input_validator, visitor_validator
from users.decorators import login_decorator

class ProductsView(View):
    @input_validator
    @visitor_validator
    def get(self, request):
        option   = request.GET.get('option', None)
        offset   = int(request.GET.get('offset', 0))
        limit    = int(request.GET.get('limit', 10))
        order    = request.GET.get('order', 'id')
        search   = request.GET.get('search', None)
        category = request.GET.get('category', 0)

        categories = {"1":'집콕KIT',"2":'전자제품',"3":'홈트레이닝', "new":"NEW", "sale":"SALE"}
        category_name = search if search else categories.get(category,'')
        
        q = Q()
        if option == 'new' or category == 'new':
            q = Q(is_new=True)
            category_name = 'NEW'

        if option == 'sale' or category == 'sale':
            q = Q(~Q(discount_percent=0))
            category_name = 'SALE'

        if (category != 'new' and category != 'sale') and category:
            q &= Q(category_id=category)
            category_name = categories[category]

        if search:
            q &= Q(name__icontains = search)
            category_name = search

        products = Product.objects.filter(q).prefetch_related('image_set')\
            .annotate(avg_rate=Avg('comment__rate'),popular=Count("userproductlike", distinct=True),review_count=Count('comment',distinct=True))\
            .order_by(order)[offset:offset+limit]

        total_count = Product.objects.filter(q).count()

        likes = None
        if request.user:
            likes = [i.id for i in Product.objects.filter(q).filter(userproductlike__user_id=request.user)[offset:offset+limit]]

        results = [{
            'id'               : product.id,
            'name'             : product.name,
            'price'            : int(product.price),
            'updated_at'       : product.updated_at.date(),
            'popular'          : product.popular,
            'avg_rate'         : round(product.avg_rate, 2) if product.avg_rate else product.avg_rate,
            'review_count'     : product.review_count,
            'is_new'           : product.is_new,
            'isLiked'          : True if likes and product.id in likes else False,
            'discount_percent' : int(product.discount_percent),
            'discounted_price' : int(product.price*(100-product.discount_percent)/100),
            'image'            : [image.url for image in product.image_set.all()],
        }for product in products]

        return JsonResponse({'results': results, 'count': total_count, 'category': category_name}, status=200)

class ProductDetailView(View):
    @visitor_validator
    def get(self, request, product_id):
        
        if not (Product.objects.filter(id=product_id).exists()):
            return JsonResponse({'MESSAGE': 'NOT_FOUND'}, status=404)
        
        product  = Product.objects.annotate(avg_rate=Avg('comment__rate'),likes=Count("userproductlike", distinct=True)\
            ,comment_count=Count('comment',distinct=True)\
                ,is_liked=Count(Case(When(Q(userproductlike__user__id=request.user)&Q(userproductlike__product__id=product_id),then=0)),distinct=True)).get(id=product_id)
        comments = Comment.objects.filter(product_id=product_id).select_related('user').prefetch_related('commentimage_set')
                
        results = {
            'id'               : product.id,
            'name'             : product.name,
            'price'            : int(product.price),
            'discount_percent' : int(product.discount_percent),
            'discounted_price' : int(product.price*(100-product.discount_percent)/100),
            'likes'            : product.likes,
            'is_new'           : product.is_new,
            'isLiked'          : product.is_liked,
            'comment_avg_rate' : round(product.avg_rate,1),
            'comment_count'    : product.comment_count,
            'images'           : [image.url for image in product.image_set.all()],
            'reviews' :[{
                "user_name"  : comment.user.name,    
                "rate"       : int(comment.rate),
                "text"       : comment.text,
                "created_at" : comment.created_at.date(),
                "images"     : [image.url for image in comment.commentimage_set.all()]
            }for comment in comments]}
                
        return JsonResponse({'results': results}, status=200)

class UserProductLikesView(View):
    @login_decorator
    def post(self, request):
        try:

            data = json.loads(request.body)

            if not data['isLiked'] :
                UserProductLike.objects.create(user_id = request.user.id, product_id = data['productId'])
                return JsonResponse({'MESSAGE':'CREATED'}, status=201)
            UserProductLike.objects.get(user_id = request.user.id, product_id = data['productId']).delete()
            return JsonResponse({'MESSAGE':'CREATED'}, status=201)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
        
        except jwt.DecodeError:
            return JsonResponse({'MESSAGE':'INVALID_AUTHORIZATION'}, status=403)
