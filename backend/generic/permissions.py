from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

from djangorestframework_camel_case.parser import CamelCaseJSONParser
from djangorestframework_camel_case.render import CamelCaseJSONRenderer

from generic import authentication

# authentication classes 分类定义
authentication_classes = {
    "basic": (authentication.CsrfExemptSessionAuthentication, BasicAuthentication, TokenAuthentication),  # 基本认证
}

# permission classes 分类定义
permission_classes = {
    "anyone": (authentication.AllowAny,),  # 允许所有
    "login": (authentication.LoginAuthenticated,),  # 只允许登录的用户
}

# parser classes 分类定义
parser_classes = {
    "underline": (JSONParser, FormParser, MultiPartParser, FileUploadParser),  # 下划线parser
    "camel_case": (CamelCaseJSONParser, JSONParser, FormParser, MultiPartParser, FileUploadParser)  # 驼峰式parser
}

# renderer classes 分类定义
renderer_classes = {
    "underline": (JSONRenderer, BrowsableAPIRenderer),  # 下划线renderer
    "camel_case": (CamelCaseJSONRenderer, JSONRenderer, BrowsableAPIRenderer)  # 驼峰式renderer
}
