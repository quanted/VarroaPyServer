# Use an official Python runtime as a parent image
FROM python:3.7.0-windowsservercore-ltsc2016

ADD https://download.microsoft.com/download/1/1/1/1116b75a-9ec3-481a-a3c8-1777b5381140/vcredist_x86.exe /vcredist.x86.exe
RUN C:\vcredist.x86.exe /quiet /install

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

RUN ["msiexec.exe", "/i", "VPPSetup.msi", "/qn"]

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
#ENV NAME World

# Run app.py when the container launches
#CMD ["python", "run_flask.py"]