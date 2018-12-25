class picture_item(object):
    def __init__(self,uid,author_name,title,picture_link,doc_id):
        self.uid = uid
        self.author_name = author_name
        self.title = title
        self.picture_link = picture_link
        self.doc_id = doc_id

    def print_bilibili_piture_json(self):
        print(
            'uid:',self.uid,','
            'author_name:',self.author_name,','
            'title:',self.title,','
            'picture_link:',self.picture_link,','
            'doc_id',self.doc_id,','
        )

    def get_picture_info(self):
        return(
            'uid:', self.uid,
            'author_name:', self.author_name,
            'title:', self.title,
            'picture_link:',self.picture_link,
            'doc_id',self.doc_id
        )
