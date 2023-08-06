# R&D toolkit


##Installation
    pip install git+https://git.identt.pl/identt/rnd-tools.git#egg=rndtools

##What is it?

### Mini-framework for keras model training

When you call `train_model` function then this framework will do few useful things:
1. it creates dirs when it do not exist
1. it automatically save architecture into `atrchitecture.json`,
1. plot model graph
1. save python source code of `get_model_function` and `training_function`,
1. after each epoch draw loss and accuray chart,
1. after each epoch save csv file with learning history.
1. saves some meta information about model, for example:
    1. processing time
    1. best train and test loss
    1. date of model creation

##### What you should do:
1. Implement `load_data` function.
1. Implement function that returns compiled keras model. Function should not have any parameters. Example:
   
   ```
   def get_model():
     model = Sequential()
     model.add(Dense(12, input_dim=8, init='uniform', activation='relu'))
     model.add(Dense(8, init='uniform', activation='relu'))
     model.add(Dense(1, init='uniform', activation='sigmoid'))

     model.compile(
       optimizer=Adam(),
       loss='binary_crossentropy',
       metrics=['accuracy']
     )

    return model
    ```
1. Implement function that trains model. Function should return model history. Example:
    ```
    def train(data, model, model_folder, callbacks=None):
        if callbacks is None:
          callbacks = []
          
        history = model.fit(data.X, data.Y, nb_epoch=150, batch_size=10, callbacks=callbacks)
        
        return history
    ```
    Pay attention to callbacks parameter. There are some extra callbacks that you should add to model callbacks.
    Also note that as in `data` parameter function pass what `load_data` function returns.

Example:

    >>> import rndtools as rnd
    >>> rnd.train.train_model(
        model_dir, 
        get_model_function=get_model, 
        training_function=train, 
        loading_data_function=load_data
    )
    
    Model path: /home/rd/notebooks/documents-detector/damian/models/in_the_wild/unet_mrz/7
    
    ------------------------------
    Creating dirs...
    ------------------------------
    ------------------------------
    Creating and compiling model...
    ------------------------------
    ------------------------------
    Saving architecture...
    ------------------------------
    ------------------------------
    Plotting model...
    ------------------------------
    ------------------------------
    Saving model source code...
    ------------------------------
    ------------------------------
    Loading data...
    ------------------------------
    ------------------------------
    Instantiating callbacks...
    ------------------------------
    ------------------------------
    Training model...
    ------------------------------
    Epoch 1/1000
    
    Finished!

    
    
### Dataset In Parts Generator
Sometimes there is so many data that it is problem to store it in memory. Then you can use divide your dataset into parts `DatasetInPartsGenerator` 
that will load this parts in turn, so you will have only part of dataset in memory.


### Pipeline
Pipeline consists of steps. Each step is a tuple of Example pipeline:

    pipeline = Pipeline(
        (
            'grayscale',
            Grayscale()
        ),
        (
            'threshold',
            Threshold()
        ),
        (
            'blur',
            Blur(
                sigma=1.5
            )
        ),
        (
            'watershed',
            Watershed(
                min_distance=5,
                threshold_rel=0.1
            )
        ),
        show_progressbar=True
    )

To create your own step just inherit from `Step` and implement `transform` method:

    from rndtools.pipeline import Step
        
    class CustomStep(Step):
        def transform(self, params):
            pass