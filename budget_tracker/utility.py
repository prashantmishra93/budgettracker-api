from rest_framework.response import Response
from rest_framework import status as http_status

class Utility:
    
    @staticmethod
    def returnFormat(message_type, data=None, query=None, error=False, http_status_code=http_status.HTTP_200_OK):
        # Define message based on query type
        if query == 'update_query':
            msg = 'You successfully updated your details !!'
        elif query == 'insert_query':
            msg = 'You successfully inserted your details !!'
        elif query == 'fetch_query':
            msg = 'You fetched data successfully !!'
        elif query == 'delete_query':
            msg = 'You deleted data successfully !!'
        elif query == 'logout_query':
            msg = 'You logged out successfully !!'
        elif query == 'login_query':
            msg = 'You have Login successfully !!'
        else:
            msg = query or 'No query action specified.'

        # Define status type
        status_str = 'SUCCESS' if message_type == 'success_msg' else 'ERROR'

        # Create standardized response body
        resp_data = {
            'status': status_str,
            'data': data,
            'message': msg,
            'error_code': error
        }
        # Return DRF Response object
        return Response(resp_data, status=http_status_code)

