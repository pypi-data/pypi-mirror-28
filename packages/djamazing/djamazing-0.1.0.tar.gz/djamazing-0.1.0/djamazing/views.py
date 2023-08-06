from django.http.response import HttpResponseForbidden, HttpResponseRedirect
from django.core.files.storage import get_storage_class

from djamazing.compat import View
from djamazing.storage import check_signature


class FileView(View):

    def __init__(self, storage=None, **kwargs):
        super(FileView, self).__init__(**kwargs)
        if storage is None:
            self.storage = get_storage_class()()
        else:
            self.storage = storage()

    def get(self, request):
        username = request.user.get_username()
        filename = request.GET['filename']
        signature = request.GET['signature']

        if not check_signature(signature, filename, username):
            return HttpResponseForbidden()
        return HttpResponseRedirect(
            redirect_to=self.storage.cloud_front_url(filename)
        )
