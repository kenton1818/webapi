from rest_framework.decorators import renderer_classes, api_view
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
import coreapi
from rest_framework import response
# noinspection PyArgumentList
@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    print("---inside schema view-----")
    schema = coreapi.Document(
    title='Price aggregator',
    url='34.92.149.102',
    description='User can get the latest second hand product information in this website, the search engine is a meta search engine. user can also record down the product data. the search api and recent product is opened for public.',
    content={
        #search the second product
        "SearchingAPI": 
            {'search': coreapi.Link(
            url='/find_my_product/Search/',
            action='get',
            fields=[
                coreapi.Field(
                    name='Keyword',
                    required=True,
                    location='query',
                    description='Input the keyword to search the second-hand product',
                    
                ),
                coreapi.Field(
                    name='seach_type',
                    location='query',
                    description='Input the Product type of what second-hand product you want to search'
                ),
                coreapi.Field(
                    name='minarea',
                    location='query',
                    description='Input the minimum   of  Product price of what second-hand product you want to search'
                ),
                coreapi.Field(
                    name='maxarea',
                    location='query',
                    description='Input the maximum   of  Product price of what second-hand product you want to search'
                ),
                
            ],
            
            description='Return the searching resuit of second-hand from different selling website API')
            },
            
        #operation about user
        "UserAPI": 
            {'login': coreapi.Link(
            url='/user/login/',
            action='post',
            fields=[
                coreapi.Field(
                    name='email',
                    required=True,
                    location='form',
                    description='login with email'
                ),
                coreapi.Field(
                    name='password',
                    required=True,
                    location='form',
                    description="The Password which match the user's email"
                ),
               
            ],
            encoding= "multipart/form-data",
            description='Return Login success if the email and password is match.'
        ),
        'logout': coreapi.Link(
            url='/user/logout/',
            action='post',  
            description='Logout the existance account without any Parameters'
        ),
        'DeleteAccount': coreapi.Link(
            url='/api/user/',
            action='delete',
            description='Delete your account of existance login with using delete request without any Parameters'
        ),
        'GetUserInfo': coreapi.Link(
            url='/api/user/',
            action='get',
            description='Get your account infomation of existance login without any Parameters '
        ),
        'SignUP': coreapi.Link(
            url='/api/user/',
            action='post',
            fields=[
                coreapi.Field(
                    name='first_name',
                    location='form',
                    description='Input first name'
                ),
                coreapi.Field(
                    name='last_name',
                    location='form',
                    description="Input  last name"
                ),
                coreapi.Field(
                    name='email',
                    required=True,
                    location='form',
                    description="Input the email"
                ),
                
                coreapi.Field(
                    name='password1',
                    required=True,
                    location='form',
                    description="Input the first password , it may match the second password"
                ),
                coreapi.Field(
                    name='password2',
                    required=True,
                    location='form',
                    description="Input the second password , it may match the first password"
                ),
               
            ],
            encoding= "multipart/form-data",
            description='Return signup success if the signup information no any mistake.'
        ),
        'UserUpdate': coreapi.Link(
            url='/api/user/',
            action='PUT',
            fields=[
                coreapi.Field(
                    name='first_name',
                    location='form',
                    description='Input the updated first name'
                ),
                coreapi.Field(
                    name='last_name',
                    location='form',
                    description="Input the updated last name"
                ),
                
                coreapi.Field(
                    name='existing_pw',
                    required=True,
                    location='form',
                    description="Input the existance password for validation"
                ),
                
                coreapi.Field(
                    name='password1',
                    required=True,
                    location='form',
                    description="Input the new password "
                ),
                coreapi.Field(
                    name='password2',
                    required=True,
                    location='form',
                    description="Input the new password again, two new password must be matched"
                ),
               
            ],
            encoding= "multipart/form-data",
            description='Return user information update success if the all information no any mistake.'
        ),
        },
        #operation about user
        "RecentProductAPI": {
            'InsertRecentProduct': coreapi.Link(
            url='/api/product/',
            action='post',
            description='no any parameters. The Api will create a table for insert recent product list from selling website, user can use get request to get a list of recent product, and use put request to update the recent product '
        ),
            'GetRecentProduct': coreapi.Link(
            url='/api/product/',
            action='get',
            description='no any parameters. it return all latest recent product data from database, moreover, it will return the recent product table is null if you are not create the recent product table with using post request'
            ),
            'UpdateRecentProduct': coreapi.Link(
            url='/api/product/',
            action='put',
            description='no any parameters. it return recent product table update success, when user want to get the latest recent product data, you should using the put request first for update the data'
        )
        },
        #operation about user's Favourite product
        "UserFavouriteProductAPI": {
            'InsertUserFavouriteProduct': coreapi.Link(
            url='/api/Favourite/',
            action='post',
            fields=[
                coreapi.Field(
                    name='price',
                    required=True,
                    location='form',
                    description="insert the price of favourtite product to the database."
                ),
                coreapi.Field(
                    name='name',
                    required=True,
                    location='form',
                    description="insert the name of favourtite product to the database."
                ),
                coreapi.Field(
                    name='link',
                    required=True,
                    location='form',
                    description="insert the selling link of favourtite product to the database."
                )
            ],
            encoding= "multipart/form-data",
            description='User can record down his favourtite product '
        ),
        'DeleteUserFavouriteProduct': coreapi.Link(
            url='/api/Favourite/',
            action='delete',
            fields=[
                coreapi.Field(
                    name='ProductID',
                    required=True,
                    location='form',
                    description="according the ID of the User Favourite Product in the databas to delete the record"
                ),
            ],
            encoding= "multipart/form-data",
            description='User can record down his favourtite product '
        ),
        'GetAllUserFavouriteProduct': coreapi.Link(
            url='/api/Favourite/',
            action='get',
            
            description="Get the existance login user's favourtite product "
        )
        }

    }
)   
    print(dir(schema))  
    # schema = generator.get_schema(request)
    return response.Response(schema)