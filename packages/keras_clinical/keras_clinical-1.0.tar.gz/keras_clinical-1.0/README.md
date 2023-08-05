# keras-clinical
Keras Implemented Clinical Model Zoo


## Purpose
To implement and expose relavent clinical models in `keras` utilizing the familiar
`keras.applications` api as a backbone.

### Test Suit
All tests are located in `keras_clinical.tests`

### Installation
`pip install keras_clinical`

### Example
```
from keras_clinical.applications.grace_mortality import GRACE_MORTALITY
gm = GRACE_MORTALITY()
gm.summary()
```

