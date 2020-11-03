class Utils:
    @staticmethod
    def split_bbox(list_of_lists: list) -> list:
        """
        Split the list of bounding box lists.
        """
        list_of_bbox = []
        for title in list_of_lists:
            title = title.split(';')
            title = title[0].split()
            title = [int(i) for i in title[1:]]
            list_of_bbox.append(title)
        return list_of_bbox

    @staticmethod
    def split_bbox_page(bbox_list: list) -> list:
        """
        DO the bbox split for class = ocr_page in tag div
        """
        for bbox in bbox_list:
            bbox = bbox.split(';')
            bbox = bbox[1].split()
            bbox = [int(i) for i in bbox[1:]]
        return bbox



