import p2p

p2p_model=p2p.main(
    epochs=2,
    enable_function=True,
    path="/Users/jonas/Downloads/tst_data",
    buffer_size=200,
    batch_size=1
)