f_path="C:\\Users\\oli\\Documents\\reps\\facade_p2p\\data\\labelmefacade-master\\labels\\sub_set"
import p2p
import tensorflow as tf

gpus = tf.config.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)
# if gpus:
#   # Restrict TensorFlow to only use the first GPU
#   try:
#     tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
    
#     logical_gpus = tf.config.experimental.list_logical_devices('GPU')
#     print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPU")
#   except RuntimeError as e:
#     # Visible devices must be set before GPUs have been initialized
#     print(e)

p2p_model=p2p.main(
    epochs=100,
    enable_function=True,
    path=f_path,
    buffer_size=200,
    batch_size=1
)