
class TagManager:

    tag_list = []
    distributed_tag_list = []

    def __init__(self, tag_file_path, num_tag_groups):
        self.tag_file_path = tag_file_path
        self.get_tags()
        self.distribute_tags(num_tag_groups)

    def get_tags(self):
        tags = open(self.tag_file_path, 'r')
        for tag in tags:
            self.tag_list.append(tag.rstrip())

    def distribute_tags(self, num_tag_groups):
        num_tags = len(self.tag_list)
        num_tags_in_group = num_tags / num_tag_groups

        current_group_start_index = 0
        current_group_end_index = current_group_start_index + num_tags_in_group
        for i in xrange(num_tag_groups):
            self.distributed_tag_list.append(self.tag_list[current_group_start_index:current_group_end_index])
            current_group_start_index += num_tags_in_group
            current_group_end_index += num_tags_in_group
