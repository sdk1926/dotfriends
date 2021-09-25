import json
import jwt

from django.http      import JsonResponse
from django.db.models import Q, Count, Avg
from django.http      import JsonResponse
from django.views     import View
from django.conf      import settings
from django.core.exceptions import FieldError, ValidationError

from .models          import Product, UserProductLike
from comments.models  import Comment
from .decorator       import query_debugger
from users.decorators import login_decorator

class PublicProductsView(View):
    def get(self, request):
        try:
            new      = request.GET.get('new', 0)
            sale     = request.GET.get('sale', 0)
            order    = request.GET.get('order', 'id')
            search   = request.GET.get('search', None)
            category = request.GET.get('category', 0)
            offset   = int(request.GET.get('offset', 0))
            limit    = int(request.GET.get('limit', 10))

            filter_set = {
                "search"   : "name__icontains",
                "new"      : "is_new",
                "sale"     : "discount_percent__gte",
                "category" : "category_id"
            }               

            q = {filter_set.get(i):v for (i,v) in request.GET.items() if filter_set.get(i)}
                            
            products = Product.objects.filter(**q).prefetch_related('image_set')\
                .annotate(avg_rate=Avg('comment__rate'),popular=Count("userproductlike", distinct=True),review_count=Count('comment',distinct=True))\
                .order_by(order)[offset:offset+limit]

            total_count = Product.objects.filter(**q).count()

            results = [{
                'id'               : product.id,
                'name'             : product.name,
                'price'            : int(product.price),
                'updated_at'       : product.updated_at.date(),
                'popular'          : product.popular,
                'avg_rate'         : round(product.avg_rate, 2) if product.avg_rate else product.avg_rate,
                'review_count'     : product.review_count,
                'is_new'           : product.is_new,
                'discount_percent' : int(product.discount_percent),
                'discounted_price' : int(product.price*(100-product.discount_percent)/100),
                'image'            : [image.url for image in product.image_set.all()],
            }for product in products]

            return JsonResponse({'results': results, 'count': total_count}, status=200)
        except ValueError:
            return JsonResponse({'MESSAGE' : 'NOT_INT'},status=401)
        except FieldError:
            return JsonResponse({'MESSAGE' : 'UNEXPECTED_VALUE1'},status=401)
        except ValidationError:
            return JsonResponse({'MESSAGE' : 'UNEXPECTED_VALUE'},status=401)

class PublicProductDetailView(View):
    def get(self, request, product_id):
        
        if not (Product.objects.filter(id=product_id).exists()):
            return JsonResponse({'MESSAGE': 'NOT_FOUND'}, status=404)
        
        product  = Product.objects.annotate(avg_rate=Avg('comment__rate'),likes=Count("userproductlike", distinct=True)\
                   ,comment_count=Count('comment',distinct=True)).get(id=product_id)
        comments = Comment.objects.filter(product_id=product_id).select_related('user').prefetch_related('commentimage_set')
                
        results = {
            'id'               : product.id,
            'name'             : product.name,
            'price'            : int(product.price),
            'discount_percent' : int(product.discount_percent),
            'discounted_price' : int(product.price*(100-product.discount_percent)/100),
            'likes'            : product.likes,
            'is_new'           : product.is_new,
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