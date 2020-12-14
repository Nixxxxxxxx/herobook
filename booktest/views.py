import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from booktest.models import HeroInfo


class HeroListView(View):
    def get(self, request):
        """页面显示图书和英雄"""
        # 获取数据库里面的数据，用json格式返回给页面
        hero_list = []
        heros = HeroInfo.objects.select_related('hbook').all()
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

        hero_dict = {
            'code': 0,
            'message': 'OK',
            'heros': hero_list,
        }

        return JsonResponse(hero_dict)

    def post(self, request):
        """接受页面数据，添加英雄到数据库"""
        json_data = json.loads(request.body)
        print(json_data)

        hero = HeroInfo.objects.create(hname=json_data['hname'], hgender=json_data['hgender'],
                                       hcomment=json_data['hcomment'], hbook_id=json_data['hbook_id'])

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


class HeroDetaiView(View):
    def get(self, request, id):
        """获取url地址id, 查询id对应的英雄"""
        hero = HeroInfo.objects.get(id=id)

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
        update_hero_dicts = json.loads(request.body)

        HeroInfo.objects.filter(id=id).update(hname=update_hero_dicts['hname'], hgender=update_hero_dicts['hgender'],
                                              hcomment=update_hero_dicts['hcomment'], hbook_id=update_hero_dicts['hbook_id'])

        hero = HeroInfo.objects.get(id=id)
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
        """获取url地址id，删除id对应的英雄"""
        HeroInfo.objects.filter(id=id).delete()

        hero_dicts = {
            "code": 0,
            "message": "OK",
        }
        return JsonResponse(hero_dicts)