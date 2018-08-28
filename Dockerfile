# Use an official Python runtime as a parent image
FROM python:3.7.0-windowsservercore-ltsc2016

ADD https://aka.ms/vs/15/release/vc_redist.x86.exe /vc_redist.x86.exe
RUN C:\vc_redist.x86.exe /quiet /install

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

RUN ["msiexec.exe", "/i", "VarroaPopSetup.msi", "/qn"]

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
#ENV NAME World

# Run app.py when the container launches
CMD ["python", "run_flask.py"]