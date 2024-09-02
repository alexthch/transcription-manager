# transcription-manager
Small program for managing transcriptions

## Installation
1. create a new conda environment. `conda create --name transcriber python=3.11`
2. activate the new conda environment. `conda activate transcriber`
3. install the following packages in the same order:
   1. PyTorch: `conda install pytorch`
   2. FFMPEG: `conda install -c conda-forge ffmpeg`
   3. WHISPER: `pip install -U openai-whisper`

4. Install this package using the command `pip install git+https://github.com/alexthch/transcription-manager.git@v1.0a`

## Example usage

In conda prompt, activate the environment
`conda activate "environment name"`
then navigate to the main folder containing the files to be transcribed.
Prompt should look like this:
`(transcriber) C:\some-folder-with-many-files-and-subfolders>`
Start by creating a settings file:
`transcribe settings -o`
Then call the command `index` to create a list of all the files to transcribe
`transcribe index`
Finally, start the transcription process by using
`transcribe start`
add `-cuda` if you have CUDA enabled gpu
`transcribe start -cuda`
