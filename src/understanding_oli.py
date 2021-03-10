f_path="C:\\Users\\oli\\Documents\\reps\\facade_p2p\\data\\labelmefacade-master\\labels\\sub_set"
import p2p

p2p_model=p2p.main(
    epochs=2,
    enable_function=True,
    path=f_path,
    buffer_size=200,
    batch_size=1
)