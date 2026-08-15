from sklearn.calibration import CalibratedClassifierCV
import pickle
from train_model import build_data
from sklearn.calibration import calibration_curve

def calibrate_model():
    with open("pred_model.pkl", "rb") as f:
        model = pickle.load(f)

    X_train, Y_train, X_test, Y_test = build_data()
    calibrated_model = CalibratedClassifierCV(model, method='sigmoid', cv=5)
    calibrated_model.fit(X_train, Y_train)

    with open("calibrated_pred_model.pkl", "wb") as s:
        pickle.dump(calibrated_model, s)

    return X_test, Y_test, calibrated_model


def prob_curve(X_test,Y_test,calibrated_model):
    probabilities = calibrated_model.predict_proba(X_test)
    home_win_probs = probabilities[:, 1]
    prob_true, prob_pred = calibration_curve(Y_test, home_win_probs, n_bins=10)
    print(prob_true, '% true')
    print(prob_pred, '% pred')



def main():
    X_test,Y_test,calibrated_model = calibrate_model()
    prob_curve(X_test,Y_test,calibrated_model)

if __name__ == "__main__":
    main()



