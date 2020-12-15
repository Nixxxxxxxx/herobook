import json
from django.views import View
from booktest.models import HeroInfo, BookInfo
from django.http import JsonResponse

# Create your views here.


#/hero/
class HeroListView(View):
    def get(self, request):
        """
        1. 从数据库查找所有的英雄和对应的书名
        2. 组织响应，返回给浏览器页面
        """
        # 1. 从数据库查找所有的英雄和对应的书名
        heros = HeroInfo.objects.all()

        # 2. 组织响应，返回给浏览器页面
        hero_list = []

        try:
            for hero in heros:
                hero_dicts = {
                    'id': hero.id,
                    'hname': hero.hname,
                    'hgender': hero.hgender,
                    'hcomment': hero.hcomment,
                    'hbook': hero.hbook.btitle,
                    'hbook_id': hero.hbook_id,
                }

                hero_list.append(hero_dicts)
        except Exception:
            return JsonResponse({
            'code': 0, 'message': '数据查询错误', 'heros': hero_list,
        })

        hero_dict = {
            'code': 0,
            'message': 'OK',
            'heros': hero_list,
        }

        return JsonResponse(hero_dict)

    def post(self, request):
        """
        1. 接受json数据，并且进行校验
        2. 向数据库添加人物数据
        3. 新增英雄数据并且返回
        """
        hname = request.json.get('hname')
        hgender = request.json.get('hname')
        hcomment = request.json.get('hname')
        hbook_id = request.json.get('hname')

        # 校验参数的完整性，客户必须传入四个参数，才能校验通过
        # 不然参数传的少了，操作数据库可能出错
        # 操作数据库要try，接受json传参要try，校验参数的完整性，接受路径传参要判断是否正确
        if not all([hname, hcomment, hbook_id]):
            return JsonResponse({'code': 400,
                                 'message': '缺少必传参数!'})

        if hgender is None:
            return JsonResponse({'code': 400,
                                 'message': '缺少必传参数!'})

        # hbook_id 是book书的外键关联属性， 判断hbook_id是否在book的id里面
        # get方法有且只能有一个值， 否则会报错
        try:
            book = BookInfo.objects.get(id=hbook_id)
        except BookInfo.DoesNotExist:
            return JsonResponse({'code': 400,
                                 'message': '图书数据不存在!'})

        try:
            hero = HeroInfo.objects.create(hname=hname, hgender=hgender,
                                       hcomment=hcomment, hbook_id=hbook_id)
        except Exception:
            return JsonResponse({'code': 400,
                                 'message': '数据库操作有误!'})

        hero_list = [{
                'id': hero.id,
                'hname': hero.hname,
                'hgender': hero.hgender,
                'hcomment': hero.hcomment,
                'hbook': hero.hbook.btitle,
                'hbook_id': hero.hbook_id,
            }]

        hero_dicts = {
            "code": 0,
            "message": "OK",
            "hero": hero_list,
        }
        return JsonResponse(hero_dicts)


# /heros/id/
# /heros/(?P<id>\d+)/
class HeroDetaiView(View):
    def get(self, request, id):
        """
        1. 获取url地址id, 查询id对应的英雄
        2.
        """
        try:
            hero = HeroInfo.objects.get(id=id)
        except HeroInfo.DoesNotExist:
            return JsonResponse({
            "code": 400,
            "message": "英雄不存在",
        })

        hero_list = [{
                'id': hero.id,
                'hname': hero.hname,
                'hgender': hero.hgender,
                'hcomment': hero.hcomment,
                'hbook': hero.hbook.btitle,
                'hbook_id': hero.hbook_id,
            }]

        hero_dicts = {
            "code": 0,
            "message": "OK",
            "hero": hero_list,
        }
        return JsonResponse(hero_dicts)

    def put(self, request, id):
        """获取url地址id，修改id对应的英雄"""
        try:
            hero = HeroInfo.objects.get(id=id)
        except HeroInfo.DoesNotExist:
            return JsonResponse({'code': 400,
                                 'message': '英雄数据不存在!'})

        hname = request.json.get('hname')
        hgender = request.json.get('hgender')
        hcomment = request.json.get('hcomment')
        hbook_id = request.json.get('hbook_id')

        if not all([hname, hcomment, hbook_id]):
            return JsonResponse({'code': 400,
                                 'message': '缺少必传参数!'})
        if hgender is None:
            return JsonResponse({'code': 400,
                                 'message': '缺少必传参数!'})

        try:
            hero.hname = hname
            hero.hgender = hgender
            hero.hcomment = hcomment
            hero.hbook_id = hbook_id
            hero.save()
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'message': '更新数据出错!'})

        hero_list = [{
                'id': hero.id,
                'hname': hero.hname,
                'hgender': hero.hgender,
                'hcomment': hero.hcomment,
                'hbook': hero.hbook.btitle,
                'hbook_id': hero.hbook_id,
            }]

        hero_dicts = {
            "code": 0,
            "message": "OK",
            "hero": hero_list,
        }
        return JsonResponse(hero_dicts)

    def delete(self, request, id):
        """
        删除指定的英雄任务
        1. 根据id找到数据库里面的指定任务
        2. 删除指定英雄
        3. 删除成功，返回响应
        """
        # 1. 根据id查找要删除的英雄对象
        try:
            hero = HeroInfo.objects.get(id=id)
        except HeroInfo.DoesNotExist:
            return JsonResponse( {
            "code": 400,
            "message": "英雄不存在",
            })

        # 2. 删除指定英雄
        try:
            # 物理删除
            # hero.delete()
            # 逻辑删除
            hero.is_delete = True
            hero.save()
        except Exception:
            return JsonResponse( {
            "code": 400,
            "message": "删除数据错误",
            })

        hero_dicts = {
            "code": 0,
            "message": "OK",
        }

        # 3. 删除成功， 返回响应
        return JsonResponse(hero_dicts)
