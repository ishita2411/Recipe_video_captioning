from youtube_transcript_api import YouTubeTranscriptApi

def get_text(vid_id):
    vid_id = vid_id
    ts = YouTubeTranscriptApi.get_transcript(vid_id, languages=['en'])
    return ts

def get_transcipts(final_frames):
    transcripts={}
    for key,value in final_frames.items():
        transcripts[key]=get_text(key)
    
    return transcripts

def get_time_array(transcipt):
   time_array=[t['start'] for t in transcipt]
   return time_array


def augmented_captions(final_frames):
    transcripts=get_transcipts(final_frames)
    captions={}
    for key,value in final_frames.items():
        time_array=get_time_array(transcripts[key])
        captions[key]=transcripts_to_captions(value,transcripts[key],time_array)
    
    return captions

def transcripts_to_captions(final_frame,transcript,time_array):
    caption=''
    lasts=''
    laste=''
    for key,value in final_frame.items():
        time_step=float(value[10:-4])
        idx=find_index(time_array,time_step,True)
        if idx!=-1 and lasts!=transcript[idx]['text']:
            caption=caption+transcript[idx]['text']+"."
            lasts=transcript[idx]['text']
        idx=find_index(time_array,time_step,False)
        if idx!=-1 and laste!=transcript[idx]['text']:
            caption=caption+transcript[idx]['text']+"."
            laste=transcript[idx]['text']
    
    return caption
    
def find_index(time_array, t, less):
  start=0
  end=len(time_array)-1
  mid=-1
  ans=-1
  if less:
    
    while start<=end:
      mid=int(start + (end-start)/2)
      if time_array[mid]<= t:
        ans=mid
        start=mid+1
      else:
        end=mid-1
    

  else:

    while start<=end:
      mid=int(start + (end-start)/2)
      if time_array[mid]>= t:
        ans=mid
        end=mid-1
      else:
        start=mid+1
    
  return int(ans)
