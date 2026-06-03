from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """自定义全局异常处理"""
    response = exception_handler(exc, context)

    if response is not None:
        # 统一错误格式
        if isinstance(response.data, dict):
            # 提取第一个错误信息
            detail = response.data.get('detail', '')
            if not detail:
                for key, value in response.data.items():
                    if isinstance(value, list):
                        detail = value[0]
                        break
                    elif isinstance(value, str):
                        detail = value
                        break
            response.data = {'error': detail or '请求失败', 'code': response.status_code}
        elif isinstance(response.data, list):
            response.data = {'error': response.data[0], 'code': response.status_code}
    else:
        # 未处理的异常返回500
        return Response(
            {'error': '服务器内部错误', 'code': 500},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
