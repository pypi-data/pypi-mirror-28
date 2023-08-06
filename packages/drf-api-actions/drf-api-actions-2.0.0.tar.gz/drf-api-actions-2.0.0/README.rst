===============
drf-api-actions
===============

提供django下rest framework的coreapi便捷调用

Quick start for django 2.0+
-----------
1. Install::

    pip install drf_api_actions>=2.0


2. [Optional] Include the drf_api_actions URLconf in your project urls.py like this::

    if settings.DEBUG:
        urlpatterns += [
            url('^', include('drf_api_actions.urls'))
        ]

    # after add this you can visit: /docs /schema /api.js

3. No migrate needed:

4. Sample::

    # Add "sample" to your INSTALLED_APPS setting like this ::
    INSTALLED_APPS = [
        ...
        'sample',
    ]

    # Include the sample URLconf in your project urls.py like this::
    urlpatterns += [
        url('^', include('sample.urls'))
    ]

    # Run server and visit /docs /schema /api.js

5. Examples::

    # Views
    class UsersAPIView(APIView):
        """
        获得用户列表

        返回值：用户列表 `['a', 'b', ...]`

        """

        def get(self, request):
            return Response(['a', 'b'])


    class UsersActionReadAPIView(ActionReadMixin, APIView):
        """
        获得用户列表, 用了`ActionReadMixin`后这是一个用 Read

        返回值：用户列表 `['a', 'b', ...]`

        """

        def get(self, request):
            return Response(['a', 'b'])


    class UsersExtraFieldsAPIView(APIView):
        """
        获得用户列表, 带user_id/user_name会过滤

        返回值：
            - 带user_id: `['a']`
            - 不带user_id: `['a','b']`
        """

        schema = AutoSchema(manual_fields=[
            coreapi.Field(name='user_id', location='query', required=True,
                          schema=coreschema.String(description='用户的id')),
        ])

        def get(self, request):
            user_id = request.GET.get('user_id', '')
            if user_id:
                return Response(['a'])
            else:
                return Response(['a', 'b'])

    # Url settings
    url('^docs/', Views.docs_as_view(title='API'))
    url('^schema/', Views.schema_as_view(title='API'))
    url('^api.js', Views.api_js_as_view(title='API'))



Quick start for django 1.0+
-----------
1. Install::

    pip install drf_api_actions==0.2.0


2. [Optional] Include the drf_api_actions URLconf in your project urls.py like this::

    if settings.DEBUG:
        urlpatterns += [
            url('^', include('drf_api_actions.urls'))
        ]

    # after add this you can visit: /docs /schema /api.js

3. No migrate needed:

4. Sample::

    # Add "sample" to your INSTALLED_APPS setting like this ::
    INSTALLED_APPS = [
        ...
        'sample',
    ]

    # Include the sample URLconf in your project urls.py like this::
    urlpatterns += [
        url('^', include('sample.urls'))
    ]

    # Run server and visit /docs /schema /api.js

5. Examples::

    # Views
    class UsersAPIView(APIView):
        """
        获得用户列表

        返回值：用户列表 `['a', 'b', ...]`

        """

        def get(self, request):
            return Response(['a', 'b'])


    class UsersActionReadAPIView(ActionReadMixin, APIView):
        """
        获得用户列表, 用了`ActionReadMixin`后这是一个用 Read

        返回值：用户列表 `['a', 'b', ...]`

        """

        def get(self, request):
            return Response(['a', 'b'])


    class UsersExtraFieldsAPIView(APIView):
        """
        获得用户列表, 带user_id/user_name会过滤

        返回值：
            - 带user_id: `['a']`
            - 不带user_id: `['a','b']`
        """

        extra_fields = [
            coreapi.Field(name='user_id', location='query', required=False,
                          schema=coreschema.String(description='用户id'))
        ]

        def get(self, request):
            user_id = request.GET.get('user_id', '')
            if user_id:
                return Response(['a'])
            else:
                return Response(['a', 'b'])

    # Url settings
    url('^docs/', Views.docs_as_view(title='API'))
    url('^schema/', Views.schema_as_view(title='API'))
    url('^api.js', Views.api_js_as_view(title='API'))

