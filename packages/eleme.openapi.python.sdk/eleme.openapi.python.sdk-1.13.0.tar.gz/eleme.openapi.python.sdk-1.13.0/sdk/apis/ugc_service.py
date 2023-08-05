# -*- coding: utf-8 -*-


# 订单评论服务
class UgcService:

    __client = None

    def __init__(self, client):
        self.__client = client

    def get_order_rate_by_order_id(self, order_id):
        """
        获取指定订单的评论
        :param orderId:订单id
        """
        return self.__client.call("eleme.ugc.getOrderRateByOrderId", {"orderId": order_id})

    def get_order_rates_by_order_ids(self, order_ids):
        """
        获取指定订单的评论
        :param orderIds:订单id
        """
        return self.__client.call("eleme.ugc.getOrderRatesByOrderIds", {"orderIds": order_ids})

    def get_unreply_order_rates_by_order_ids(self, order_ids):
        """
        获取未回复的评论
        :param orderIds:订单id
        """
        return self.__client.call("eleme.ugc.getUnreplyOrderRatesByOrderIds", {"orderIds": order_ids})

    def get_order_rates_by_shop_id(self, shop_id, start_time, end_time, offset, page_size):
        """
        获取指定店铺的评论
        :param shopId: 餐厅id
        :param startTime:  开始时间,只能查询最近90天的数据
        :param endTime:  结束时间
        :param offset:页面偏移量
        :param pageSize:页面大小
        """
        return self.__client.call("eleme.ugc.getOrderRatesByShopId", {"shopId": shop_id, "startTime": start_time, "endTime": end_time, "offset": offset, "pageSize": page_size})

    def get_order_rates_by_shop_ids(self, shop_ids, start_time, end_time, offset, page_size):
        """
        获取指定店铺的评论
        :param shopIds:店铺id
        :param startTime:  开始时间,只能查询最近90天的数据
        :param endTime:  结束时间
        :param offset:页面偏移量
        :param pageSize:页面大小
        """
        return self.__client.call("eleme.ugc.getOrderRatesByShopIds", {"shopIds": shop_ids, "startTime": start_time, "endTime": end_time, "offset": offset, "pageSize": page_size})

    def get_unreply_order_rates_by_shop_ids(self, shop_ids, start_time, end_time, offset, page_size):
        """
        获取未回复的评论
        :param shopIds:店铺id
        :param startTime:  开始时间,只能查询最近90天的数据
        :param endTime:  结束时间
        :param offset:页面偏移量
        :param pageSize:页面大小
        """
        return self.__client.call("eleme.ugc.getUnreplyOrderRatesByShopIds", {"shopIds": shop_ids, "startTime": start_time, "endTime": end_time, "offset": offset, "pageSize": page_size})

    def get_order_rates_by_shop_and_rating(self, shop_id, score, start_time, end_time, offset, page_size):
        """
        获取店铺的满意度评价信息
        :param shopId: 餐厅id
        :param score:满意度,取值范围为1~5，1为最不满意，5为非常满意
        :param startTime:  开始时间,只能查询最近90天的数据
        :param endTime:  结束时间
        :param offset:页面偏移量
        :param pageSize:页面大小
        """
        return self.__client.call("eleme.ugc.getOrderRatesByShopAndRating", {"shopId": shop_id, "score": score, "startTime": start_time, "endTime": end_time, "offset": offset, "pageSize": page_size})

    def get_item_rates_by_item_id(self, item_id, start_time, end_time, offset, page_size):
        """
        获取单个商品的评论
        :param itemId: 商品id
        :param startTime:  开始时间,只能查询最近90天的数据
        :param endTime:  结束时间
        :param offset:页面偏移量
        :param pageSize:页面大小
        """
        return self.__client.call("eleme.ugc.getItemRatesByItemId", {"itemId": item_id, "startTime": start_time, "endTime": end_time, "offset": offset, "pageSize": page_size})

    def get_item_rates_by_item_ids(self, item_ids, start_time, end_time, offset, page_size):
        """
        获取多个商品的评论
        :param itemIds:商品id
        :param startTime:  开始时间,只能查询最近90天的数据
        :param endTime:  结束时间
        :param offset:页面偏移量
        :param pageSize:页面大小
        """
        return self.__client.call("eleme.ugc.getItemRatesByItemIds", {"itemIds": item_ids, "startTime": start_time, "endTime": end_time, "offset": offset, "pageSize": page_size})

    def get_unreply_item_rates_by_item_ids(self, item_ids, start_time, end_time, offset, page_size):
        """
        获取多个商品未回复的评论
        :param itemIds:店铺id
        :param startTime:  开始时间,只能查询最近90天的数据
        :param endTime:  结束时间
        :param offset:页面偏移量
        :param pageSize:页面大小
        """
        return self.__client.call("eleme.ugc.getUnreplyItemRatesByItemIds", {"itemIds": item_ids, "startTime": start_time, "endTime": end_time, "offset": offset, "pageSize": page_size})

    def reply_rate_by_rate_id(self, rate_id, reply_type, reply):
        """
        回复指定类型的评论
        :param rateId:评论编号
        :param replyType:评论类型
        :param reply:回复的内容
        """
        return self.__client.call("eleme.ugc.replyRateByRateId", {"rateId": rate_id, "replyType": reply_type, "reply": reply})

    def reply_rate_by_rate_ids(self, rate_ids, reply_type, reply):
        """
        回复指定类型的评论
        :param rateIds: 评论编号
        :param replyType:评论类型
        :param reply:回复的内容
        """
        return self.__client.call("eleme.ugc.replyRateByRateIds", {"rateIds": rate_ids, "replyType": reply_type, "reply": reply})

    def reply_rate_by_order_id(self, order_id, reply):
        """
        回复订单未回复的评论
        :param orderId:订单id
        :param reply:回复内容
        """
        return self.__client.call("eleme.ugc.replyRateByOrderId", {"orderId": order_id, "reply": reply})

    def reply_comment_by_order_ids(self, order_ids, reply):
        """
        批量回复订单未回复的评论
        :param orderIds:订单id
        :param reply:回复信息
        """
        return self.__client.call("eleme.ugc.replyCommentByOrderIds", {"orderIds": order_ids, "reply": reply})

    def reply_rates_by_item_id(self, item_id, reply, start_time, end_time):
        """
        回复商品回复的评论
        :param itemId:商品id
        :param reply:回复内容
        :param startTime:  开始时间,只能查询最近90天的数据
        :param endTime:  结束时间
        """
        return self.__client.call("eleme.ugc.replyRatesByItemId", {"itemId": item_id, "reply": reply, "startTime": start_time, "endTime": end_time})

    def reply_rates_by_item_ids(self, item_ids, reply, start_time, end_time):
        """
        回复多个商品评论
        :param itemIds:商品d
        :param reply:回复信息
        :param startTime:开始时间,只能查询最近90天的数据
        :param endTime:结束时间
        """
        return self.__client.call("eleme.ugc.replyRatesByItemIds", {"itemIds": item_ids, "reply": reply, "startTime": start_time, "endTime": end_time})

    def reply_rate_by_rate_id_and_shop_id(self, rate_id, shop_id, reply_type, reply):
        """
        通过rateId和shopId 回复指定类型的评论
        :param rateId:评论编号
        :param shopId: 餐厅id
        :param replyType:评论类型
        :param reply:回复的内容
        """
        return self.__client.call("eleme.ugc.replyRateByRateIdAndShopId", {"rateId": rate_id, "shopId": shop_id, "replyType": reply_type, "reply": reply})

    def reply_rate_by_rate_ids_and_shop_id(self, rate_ids, shop_id, reply_type, reply):
        """
        通过rateIds和shopId 批量回复指定类型的评论
        :param rateIds: 评论编号
        :param shopId: 餐厅id
        :param replyType:评论类型
        :param reply:回复的内容
        """
        return self.__client.call("eleme.ugc.replyRateByRateIdsAndShopId", {"rateIds": rate_ids, "shopId": shop_id, "replyType": reply_type, "reply": reply})

