from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Dict, Union, Any



class DownloaderOptions(BaseModel):
    http_chunk_size: Optional[int] = None

class Fragment(BaseModel):
    url: Optional[str] = None
    duration: Optional[float] = None

class HttpHeaders(BaseModel):
    user_agent: Optional[str] = Field(default=None, alias="User-Agent")
    accept: Optional[str] = Field(default=None, alias="Accept")
    accept_language: Optional[str] = Field(default=None, alias="Accept-Language")
    sec_fetch_mode: Optional[str] = Field(default=None, alias="Sec-Fetch-Mode")

class Format(BaseModel):
    asr: Optional[int] = None
    filesize: Optional[int] = None
    source_preference: Optional[int] = None
    audio_channels: Optional[int] = None
    quality: Optional[float] = None
    has_drm: Optional[bool] = None
    language: Optional[str] = None
    language_preference: Optional[int] = None
    preference: Optional[Any] = None
    dynamic_range: Optional[str] = None
    downloader_options: Optional[DownloaderOptions] = DownloaderOptions(http_chunk_size=None)
    format_id: Optional[str] = None
    format_note: Optional[str] = None
    ext: Optional[str] = None
    protocol: Optional[str] = None
    acodec: Optional[str] = None
    vcodec: Optional[str] = None
    url: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    fps: Optional[float] = None
    rows: Optional[int] = None
    columns: Optional[int] = None
    fragments: Optional[List[Fragment]] =  Field(
        default_factory=lambda: [Fragment(url=None, duration=None)]
    )
    container: Optional[str] = None
    audio_ext: Optional[str] = None
    video_ext: Optional[str] = None
    vbr: Optional[float] = None
    abr: Optional[float] = None
    tbr: Optional[float] = None
    resolution: Optional[str] = None
    aspect_ratio: Optional[float] = None
    filesize_approx: Optional[int] = None
    http_headers: Optional[HttpHeaders] = None
    format: Optional[Union[Dict, str]] = None

    @model_validator(mode='before')
    def convert_http_headers(cls, values):
        if 'http_headers' in values:
            # Convert the dictionary to a HttpHeaders instance
            values['http_headers'] = HttpHeaders(**values['http_headers'])
        return values

    def getExtension(self):
        """Returns the recommended file extension based on the resolution."""
        return "mp3" if self.resolution == "audio only" else (self.ext or "unknown")

        
    def to_dict(self) -> Dict:
        """Converts the Format instance to a dictionary, handling nested BaseModel objects."""
        return dict(sorted(self.model_dump(by_alias=True, exclude_none=False).items()))


