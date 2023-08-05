# -*- coding: utf-8 -*-


# 活动服务
class ActivityService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def create_coupon_activity(self, create_info):
        """
        创建代金券活动
        :param createInfo:创建代金券活动的结构体
        """
        return self.__client.call("eleme.activity.coupon.createCouponActivity", {"createInfo": create_info})

    def give_out_coupons(self, shop_id, coupon_activity_id, mobiles):
        """
        向指定用户发放代金券
        :param shopId:店铺Id
        :param couponActivityId:代金券活动Id
        :param mobiles:需要发放代金券的用户手机号列表
        """
        return self.__client.call("eleme.activity.coupon.giveOutCoupons", {"shopId": shop_id, "couponActivityId": coupon_activity_id, "mobiles": mobiles})

    def query_coupon_activities(self, shop_id, coupon_activity_type, activity_status, page_no, page_size):
        """
        分页查询店铺代金券活动信息
        :param shopId:店铺Id
        :param couponActivityType:代金券活动类型
        :param activityStatus:活动状态
        :param pageNo:页码（第几页）
        :param pageSize:每页数量
        """
        return self.__client.call("eleme.activity.coupon.queryCouponActivities", {"shopId": shop_id, "couponActivityType": coupon_activity_type, "activityStatus": activity_status, "pageNo": page_no, "pageSize": page_size})

    def query_received_coupon_details(self, shop_id, coupon_activity_id, coupon_status, page_no, page_size):
        """
        分页查询店铺代金券领取详情
        :param shopId:店铺Id
        :param couponActivityId:代金券活动Id
        :param couponStatus:代金券状态
        :param pageNo:页码（第几页）
        :param pageSize:每页数量
        """
        return self.__client.call("eleme.activity.coupon.queryReceivedCouponDetails", {"shopId": shop_id, "couponActivityId": coupon_activity_id, "couponStatus": coupon_status, "pageNo": page_no, "pageSize": page_size})

    def query_invited_food_activities(self, shop_id):
        """
        通过店铺Id查询该店铺被邀约的美食活动
        :param shopId:店铺Id
        """
        return self.__client.call("eleme.activity.food.queryInvitedFoodActivities", {"shopId": shop_id})

    def apply_food_activity(self, activity_id, activity_apply_info):
        """
        报名美食活动
        :param activityId:活动Id
        :param activityApplyInfo:活动报名信息
        """
        return self.__client.call("eleme.activity.food.applyFoodActivity", {"activityId": activity_id, "activityApplyInfo": activity_apply_info})

    def query_food_activities(self, activity_id, shop_id, page_no, page_size):
        """
        通过店铺Id和活动Id分页查询店铺已报名的美食活动
        :param activityId:活动Id
        :param shopId:店铺Id
        :param pageNo:页码
        :param pageSize:每页数量
        """
        return self.__client.call("eleme.activity.food.queryFoodActivities", {"activityId": activity_id, "shopId": shop_id, "pageNo": page_no, "pageSize": page_size})

    def update_food_activity_item_stock(self, activity_id, shop_id, item_id, stock):
        """
        修改美食活动的菜品库存
        :param activityId:活动Id
        :param shopId:店铺Id
        :param itemId:菜品Id
        :param stock:库存
        """
        return self.__client.call("eleme.activity.food.updateFoodActivityItemStock", {"activityId": activity_id, "shopId": shop_id, "itemId": item_id, "stock": stock})

    def offline_food_activity_item(self, activity_id, shop_id, item_id):
        """
        取消参与了美食活动的菜品
        :param activityId:活动Id
        :param shopId:店铺Id
        :param itemId:菜品Id
        """
        return self.__client.call("eleme.activity.food.offlineFoodActivityItem", {"activityId": activity_id, "shopId": shop_id, "itemId": item_id})

    def unbind_food_activity(self, activity_id, shop_id):
        """
        作废店铺与美食活动的关联关系
        :param activityId:活动Id
        :param shopId:店铺Id
        """
        return self.__client.call("eleme.activity.food.unbindFoodActivity", {"activityId": activity_id, "shopId": shop_id})

    def get_invited_activity_infos(self, shop_id):
        """
        查询店铺邀约活动信息
        :param shopId:店铺Id
        """
        return self.__client.call("eleme.activity.flash.getInvitedActivityInfos", {"shopId": shop_id})

    def apply_flash_activity(self, activity_id, activity_apply_info):
        """
        报名限量抢购活动
        :param activityId:活动Id
        :param activityApplyInfo:活动报名信息
        """
        return self.__client.call("eleme.activity.flash.applyFlashActivity", {"activityId": activity_id, "activityApplyInfo": activity_apply_info})

    def get_activity_apply_infos(self, activity_id, shop_id, page_no, page_size):
        """
        通过店铺Id和活动Id分页查询报名详情
        :param activityId:活动Id
        :param shopId:店铺Id
        :param pageNo:页码
        :param pageSize:每页数量
        """
        return self.__client.call("eleme.activity.flash.getActivityApplyInfos", {"activityId": activity_id, "shopId": shop_id, "pageNo": page_no, "pageSize": page_size})

    def update_activity_item_stock(self, activity_id, shop_id, item_id, stock):
        """
        修改活动菜品库存
        :param activityId:活动Id
        :param shopId:店铺Id
        :param itemId:菜品Id
        :param stock:库存
        """
        return self.__client.call("eleme.activity.flash.updateActivityItemStock", {"activityId": activity_id, "shopId": shop_id, "itemId": item_id, "stock": stock})

    def offline_flash_activity_item(self, activity_id, shop_id, item_id):
        """
        取消活动菜品
        :param activityId:活动Id
        :param shopId:店铺Id
        :param itemId:菜品Id
        """
        return self.__client.call("eleme.activity.flash.offlineFlashActivityItem", {"activityId": activity_id, "shopId": shop_id, "itemId": item_id})

    def invalid_shop_activity(self, activity_id, shop_id):
        """
        作废店铺与活动的关联关系
        :param activityId:活动Id
        :param shopId:店铺Id
        """
        return self.__client.call("eleme.activity.flash.invalidShopActivity", {"activityId": activity_id, "shopId": shop_id})

