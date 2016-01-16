from tweepy import Stream


class CustomStream(Stream):
    listener = None
    auth_handler = None
    filter_track = []

    def __init__(self, listener, auth_handler, filter_track):
        self.listener = listener
        self.auth_handler = auth_handler
        self.filter_track = filter_track
        super(CustomStream, self).__init__(self.auth_handler, self.listener)

    def stream(self, async):
        self.filter(track=self.filter_track, async=async)



