<h1>Facial Recognition with OpenCV</h1>

<h2>Installing Requirements </h2>
It is recommended that you create a new virtualenv when you install these packages <br>

To install the required packages, do
``` pip install -r requirements.txt```

<h2>Extracting Facial Data</h2>
To extract facial data, create a folder called Datasets, and create individual folders inside them with the names corresponding to the facial data labels <br>

Create another folder called `output` to save the pickle files with the embeddings

Run the `extract_embeddings.py` file to extract Facial data<br>

``` python extract_embeddings.py```

<h2>Training the Model <h2>

Once you've extracted the features, run the `train_model.py` to train your model to the dataset.

```python train_model.py```

<h2>Recognising Faces</h2>

After the model training, to detect faces from video, run the `recognise_video.py` to recognise from video

```pythin recognise_video.py```
