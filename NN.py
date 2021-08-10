import tensorflow as tf

try:
    model_bet0 = tf.keras.models.load_model("weights/model_bet0")
    model_bet0.load_weights("weights/model_bet0.h5")
    model_bet1 = tf.keras.models.load_model("weights/model_bet1")
    model_bet1.load_weights("weights/model_bet1.h5")
    model_bet2 = tf.keras.models.load_model("weights/model_bet2")
    model_bet2.load_weights("weights/model_bet2.h5")
    model_bet3 = tf.keras.models.load_model("weights/model_bet3")
    model_bet3.load_weights("weights/model_bet3.h5")
    model_bet = {0: model_bet0, 1: model_bet1, 2: model_bet2, 3: model_bet3}
    print("Networks for betting have been loaded")
except:
    print("Networks for betting should be build")
    model_bet0 = tf.keras.Sequential([
        tf.keras.layers.Dense(52, activation="relu", input_dim=52),
        tf.keras.layers.Dense(52, activation="relu"),
        tf.keras.layers.Dense(14, activation="softmax")
    ])
    model_bet0.compile(optimizer='adam',
                       loss="mse",
                       metrics=['accuracy'])

    model_bet0.save("weights/model_bet0")

    model_bet1 = tf.keras.Sequential([
        tf.keras.layers.Dense(53, activation="relu", input_dim=53),
        tf.keras.layers.Dense(53, activation="relu"),
        tf.keras.layers.Dense(14, activation="softmax")
    ])
    model_bet1.compile(optimizer='adam',
                       loss="mse",
                       metrics=['accuracy'])

    model_bet1.save("weights/model_bet1")

    model_bet2 = tf.keras.Sequential([
        tf.keras.layers.Dense(54, activation="relu", input_dim=54),
        tf.keras.layers.Dense(54, activation="relu"),
        tf.keras.layers.Dense(14, activation="softmax")
    ])
    model_bet2.compile(optimizer='adam',
                       loss="mse",
                       metrics=['accuracy'])

    model_bet2.save("weights/model_bet2")

    model_bet3 = tf.keras.Sequential([
        tf.keras.layers.Dense(55, activation="relu", input_dim=55),
        tf.keras.layers.Dense(55, activation="relu"),
        tf.keras.layers.Dense(14, activation="softmax")
    ])
    model_bet3.compile(optimizer='adam',
                       loss="mse",
                       metrics=['accuracy'])

    model_bet3.save("weights/model_bet3")

    model_bet = {0: model_bet0, 1: model_bet1, 2: model_bet2, 3: model_bet3}


def save_model_bet():
    for i in range(4):
        model_bet[i].save_weights("weights/model_bet" + str(i) + ".h5")


try:
    model_play0 = tf.keras.models.load_model("weights/model_play0")
    model_play0.load_weights("weights/model_play0.h5")
    model_play1 = tf.keras.models.load_model("weights/model_play1")
    model_play0.load_weights("weights/model_play1.h5")
    model_play2 = tf.keras.models.load_model("weights/model_play2")
    model_play2.load_weights("weights/model_play2.h5")
    model_play3 = tf.keras.models.load_model("weights/model_play3")
    model_play3.load_weights("weights/model_play3.h5")
    model_play = {0: model_play0, 1: model_play1, 2: model_play2, 3: model_play3}
    print("Networks for playing have been loaded")
except:
    print("Networks for playing should be build")
    model_play0 = tf.keras.Sequential([
        tf.keras.layers.Dense(260, activation="relu", input_dim=260),  # 5*4*13=260
        tf.keras.layers.Dense(260, activation="relu"),
        tf.keras.layers.Dense(260, activation="relu"),
        tf.keras.layers.Dense(52, activation="softmax")  # 4*13=52
    ])
    model_play0.compile(optimizer='adam',
                        loss="mse",
                        metrics=['accuracy'])

    model_play0.save("weights/model_play0")

    model_play1 = tf.keras.Sequential([
        tf.keras.layers.Dense(260, activation="relu", input_dim=260),  # 5*4*13=260
        tf.keras.layers.Dense(260, activation="relu"),
        tf.keras.layers.Dense(260, activation="relu"),
        tf.keras.layers.Dense(52, activation="softmax")  # 4*13=52
    ])
    model_play1.compile(optimizer='adam',
                        loss="mse",
                        metrics=['accuracy'])

    model_play1.save("weights/model_play1")

    model_play2 = tf.keras.Sequential([
        tf.keras.layers.Dense(260, activation="relu", input_dim=260),  # 5*4*13=260
        tf.keras.layers.Dense(260, activation="relu"),
        tf.keras.layers.Dense(260, activation="relu"),
        tf.keras.layers.Dense(52, activation="softmax")  # 4*13=52
    ])
    model_play2.compile(optimizer='adam',
                        loss="mse",
                        metrics=['accuracy'])

    model_play2.save("weights/model_play2")

    model_play3 = tf.keras.Sequential([
        tf.keras.layers.Dense(260, activation="relu", input_dim=260),  # 5*4*13=260
        tf.keras.layers.Dense(260, activation="relu"),
        tf.keras.layers.Dense(260, activation="relu"),
        tf.keras.layers.Dense(52, activation="softmax")  # 4*13=52
    ])
    model_play3.compile(optimizer='adam',
                        loss="mse",
                        metrics=['accuracy'])

    model_play3.save("weights/model_play3")

    model_play = {0: model_play0, 1: model_play1, 2: model_play2, 3: model_play3}


def save_model_play():
    for i in range(4):
        model_play[i].save_weights("weights/model_play" + str(i) + ".h5")

