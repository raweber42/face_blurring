class VideoState:
  def __init__(self, stream_stopped, blur_level):
    self.stream_stopped = stream_stopped
    self.blur_level = blur_level
  
  def update_blur_level(self, new_value):
    self.blur_level = new_value

  def update_stream_status(self, new_status):
    self.stream_stopped = new_status

video_state = VideoState(False, 13)
