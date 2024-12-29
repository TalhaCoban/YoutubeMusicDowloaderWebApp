from pydantic import BaseModel
from typing import List, Optional, Dict

from models.format import Format
from models.thumbnail import Thumbnail
from models.caption import Caption


none_types = ['none', 'None', None, 'null']

class Video(BaseModel):
    
    id: Optional[str] = None
    title: Optional[str] = None
    formats: Optional[List[Format]] = None
    thumbnails: Optional[List[Thumbnail]] = None
    thumbnail: Optional[str] = None
    description: Optional[str] = None
    channel_id: Optional[str] = None
    channel_url: Optional[str] = None
    duration: Optional[int] = None
    view_count: Optional[int] = None
    average_rating: Optional[float] = None
    age_limit: Optional[int] = None
    webpage_url: Optional[str] = None
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    playable_in_embed: Optional[bool] = False
    like_count: Optional[int] = None
    channel: Optional[str] = None
    channel_follower_count: Optional[int] = None
    availability: Optional[str] = None
    fulltitle: Optional[str] = None
    duration_string: Optional[str] = None
    fps: Optional[int] = None
    automatic_captions: Optional[Dict[str, List[Caption]]] = None
    
    def getAllVideoFormats(self):
        return [f for f in self.formats
                      if f.vcodec not in none_types and f.acodec in none_types and f.format_note not in none_types]
        
    def getAllAudioFormats(self, video_format_id: Optional[str] = None):
        if video_format_id in none_types:
            return [f for f in self.formats if (
                f.acodec not in none_types and f.vcodec in none_types)]
        else:
            video_format_ext = self.findVideoFormatById(video_format_id).ext
            audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[video_format_ext]
            return [f for f in self.formats if (
                f.acodec not in none_types and f.vcodec in none_types and f.ext == audio_ext)]

    def findFormatById(self, id: str):
        for format in self.formats:
            if format.format_id == id:
                return format

    def findVideoFormatById(self, id: str):
        for format in self.formats:
            if format.resolution != "audio only":
                if format.format_id == id:
                    return format
                
    def findAudioFormatById(self, id: str):
        for format in self.formats:
            if format.resolution == "audio only":
                if format.format_id == id:
                    return format
                
    def to_dict(self) -> Dict:
        """Converts the Format instance to a dictionary, handling nested BaseModel objects."""
        return dict(sorted(self.model_dump(by_alias=True, exclude_none=False).items()))


        
