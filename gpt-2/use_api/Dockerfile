FROM tensorflow/tensorflow:2.2.0
RUN pip install --no-cache-dir fastapi
RUN pip install scikit-learn
RUN pip install numpy
RUN pip install tensorflow_hub
RUN pip install uvicorn
RUN python -c "import tensorflow_hub as hub; hub.load('https://tfhub.dev/google/universal-sentence-encoder-large/5');"
COPY ./use_app.py use_app.py
EXPOSE 8000
ENTRYPOINT ["uvicorn", "use_app:app", "--host", "0.0.0.0"]
