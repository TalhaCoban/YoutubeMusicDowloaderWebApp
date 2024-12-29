from pydantic import BaseModel, Field
from typing import Optional
from models.format import Format


class Options(BaseModel):
    
    format: Optional[str] = Field(default=None)
    outtmpl: Optional[str] = Field(default=None)
    quiet: Optional[bool] = Field(default=None) 
    
    def to_dict(self):
        return self.model_dump(exclude_none=True)
    

class YDLOptions():

    videoFormat: Optional[Format]
    audioFormat: Optional[Format]
    title: Optional[str]
    ext: Optional[str]
    quiet: Optional[bool]
    
    def __init__(self, video):
        self.videoFormat = None
        self.audioFormat = None
        self.title = None
        self.ext = None
        self.quiet = None
        self.video = video

    @staticmethod
    def getSearchOptions():
        return { "quiet": True }
    
    def setVideoFormat(self, format_id: Optional[str] = None):
        if format_id == None:
            self.videoFormat = None
        else:
            format = self.video.findVideoFormatById(format_id)
            if format != None:
                self.videoFormat = format
                self.ext = format.ext
            else:
                raise Exception(f"there is no format with format_id = {format_id}")
        
    def setAudioFormat(self, format_id: Optional[str] = None):
        if format_id == None:
            self.audioFormat = None
        else:
            format = self.video.findAudioFormatById(format_id)
            if format != None:
                self.audioFormat = format
                if self.videoFormat == None:
                    self.ext = format.getExtension()
            else:
                raise Exception(f"there is no format with format_id = {format_id}")
            
    def setTitle(self, title):
        self.title = title
        
    def setQuiet(self, state: bool):
        self.quiet = state
        
    def createOptions(self, stream: Optional[bool] = False):
        formatList = []
        if self.videoFormat != None:
            formatList.append(self.videoFormat.format_id)
        if self.audioFormat != None:
            formatList.append(self.audioFormat.format_id)
        if len(formatList) == 0:
            raise Exception("There is format set to neither audio nor video")
        if self.title == None:
            format_note = self.videoFormat.format_note if self.videoFormat != None else ""
            self.title = f"{self.video.title}.{format_note}".rstrip(".")
        if stream:
            outtmpl = "-"
        else:
            outtmpl =  f'{self.title}.{self.ext}'
        format = "+".join(formatList)
        options = Options(format=format, outtmpl=outtmpl)
        if self.quiet != None:
            options.quiet = self.quiet
        return options
        
    def getYDLOptionsDict(self, stream: Optional[bool] = False):
        return self.createOptions(stream).to_dict()
    
    def getYDLOptionsObject(self, stream: Optional[bool] = False):
        return self.createOptions(stream)
        
    def to_dict(self):
        return self.__dict__
