
# Logistic Regression using PyTorch with L-BFGS optimization
# predict sex from age, county, monocyte, history
# PyTorch 1.8.0-CPU Anaconda3-2020.02  Python 3.7.6
# Windows 10

import numpy as np
import torch as T

device = T.device("cpu")  # apply to Tensor or Module


#        1         2         3         4         5         6
# 3456789012345678901234567890123456789012345678901234567890
# ----------------------------------------------------------
# 数据集的创建，继承T.utils.data.Dataset
class PatientDataset(T.utils.data.Dataset):
    # sex age   county    monocyte  hospitalization history
    # sex: 0 = male, 1 = female
    # county: austin, bailey, carson
    # history: minor, moderate, major

    def __init__(self, src_file, num_rows=None):
        # 从文件中读取数据
        all_data = np.loadtxt(src_file, max_rows=num_rows,
                              usecols=range(0, 9), delimiter="\t", skiprows=0,
                              comments="#", dtype=np.float32)  # read all 9 columns

        self.x_data = T.tensor(all_data[:, 1:9],
                               dtype=T.float32).to(device)
        # 这里的话self.y_data的shape是200
        self.y_data = T.tensor(all_data[:, 0],
                               dtype=T.float32).to(device)
        # 改了过后的shape是200*1
        self.y_data = self.y_data.reshape(-1, 1)  # 2D required

    def __len__(self):
        return len(self.x_data)

    def __getitem__(self, idx):
        preds = self.x_data[idx, :]  # idx rows, all 8 cols
        sex = self.y_data[idx, :]  # idx rows, the only col
        sample = {'predictors': preds, 'sex': sex}
        return sample


# ---------------------------------------------------------

class LogisticReg(T.nn.Module):
    def __init__(self):
        super(LogisticReg, self).__init__()
        self.fc = T.nn.Linear(8, 1)
        # 初始化神经网络参数值
        T.nn.init.uniform_(self.fc.weight, -0.01, 0.01)
        T.nn.init.zeros_(self.fc.bias)

    def forward(self, x):
        z = self.fc(x)
        p = T.sigmoid(z)
        return p


# ----------------------------------------------------------

def train(log_reg, ds, mi):
    log_reg.train() # 模式为train
    # model, dataset, batch size, max iterations
    # batch size must equal all data for L-BFGS
    # learn_rate not applicable
    # max_epochs is really max iterations
    # log_every isn't needed -- typically very few iterations

    # log_reg.train()  # set training mode not relevant
    # loss_func = T.nn.MSELoss()  # mean squared error - NO
    loss_func = T.nn.SoftMarginLoss()  # binary cross entropy
    # opt = T.optim.SGD(log_reg.parameters(), lr=lr)
    opt = T.optim.LBFGS(log_reg.parameters(), max_iter=mi)
    train_ldr = T.utils.data.DataLoader(ds,
                                        batch_size=10, shuffle=True)  # shuffle irrelevant

    print("\nStarting L-BFGS training")

    for itr in range(0, mi):
        itr_loss = 0.0  # for one iteration
        for (_, all_data) in enumerate(train_ldr):  # b_ix irrelevant
            X = all_data['predictors']  # [10,8]  inputs
            Y = all_data['sex']  # [10,1]  targets

            # -------------------------------------------
            def loss_closure():
                opt.zero_grad()
                oupt = log_reg(X)
                loss_val = loss_func(oupt, Y)
                loss_val.backward()
                return loss_val

            # -------------------------------------------

            opt.step(loss_closure)  # get loss, use to update wts

            oupt = log_reg(X)  # monitor loss
            loss_val = loss_closure()
            itr_loss += loss_val.item()
        print("iteration = %4d   loss = %0.4f" % (itr, itr_loss))

    print("Done ")


# ----------------------------------------------------------

def accuracy(model, ds, verbose=False):
    # ds is a iterable Dataset of Tensors
    model.eval()
    n_correct = 0;
    n_wrong = 0

    for i in range(len(ds)):
        inpts = ds[i]['predictors']
        target = ds[i]['sex']  # float32  [0.0] or [1.0]
        with T.no_grad():
            oupt = model(inpts)
        if verbose == True:
            print("")
            print(oupt)
            print(target)
            input()

        # avoid 'target == 1.0'
        if target < 0.5 and oupt < 0.5:  # .item() not needed
            n_correct += 1
        elif target >= 0.5 and oupt >= 0.5:
            n_correct += 1
        else:
            n_wrong += 1

    return (n_correct * 1.0) / (n_correct + n_wrong)


# ----------------------------------------------------------

def main():
    # 0. get started
    print("\nPatient gender logisitic regression L-BFGS PyTorch ")
    print("Predict gender from age, county, monocyte, history")
    T.manual_seed(1)
    np.random.seed(1)

    # 1. create Dataset and DataLoader objects
    print("\nCreating Patient train and test Datasets ")

    train_file = "patients_train.txt"
    test_file = "patients_test.txt"

    train_ds = PatientDataset(train_file)  # read all rows
    test_ds = PatientDataset(test_file)

    # 2. create model
    print("\nCreating 8-1 logistic regression model ")
    log_reg = LogisticReg().to(device)

    # 3. train network
    print("\nPreparing L-BFGS training")
    # bat_size = len(train_ds)  # use all
    # lrn_rate = 0.10
    max_iterations = 1000
    # ep_log_interval = 200
    print("Loss function: BCELoss ")
    print("Optimizer: L-BFGS ")
    # print("Learn rate: " + str(lrn_rate))
    # print("Batch size: " + str(bat_size))
    # print("Max epochs: " + str(max_epochs))

    # train(log_reg, train_ds, bat_size, lrn_rate, max_epochs,
    #   ep_log_interval)
    train(log_reg, train_ds, max_iterations)

    # ----------------------------------------------------------

    # 4. evaluate model
    acc_train = accuracy(log_reg, train_ds)
    print("\nAccuracy on train data = %0.2f%%" % \
          (acc_train * 100))
    acc_test = accuracy(log_reg, test_ds, verbose=False)
    print("Accuracy on test data = %0.2f%%" % \
          (acc_test * 100))

    # 5. examine model
    wts = log_reg.fc.weight.data
    print("\nModel weights: ")
    print(wts)
    bias = log_reg.fc.bias.data
    print("Model bias: ")
    print(bias)

    # 6. save model
    # print("Saving trained model state_dict \n")
    # path = ".\\Models\\patients_LR_model.pth"
    # T.save(log_reg.state_dict(), path)

    # 7. make a prediction
    print("Predicting sex for age = 30, county = carson, ")
    print("monocyte count = 0.4000, ")
    print("hospitization history = moderate ")
    inpt = np.array([[0.30, 0, 0, 1, 0.40, 0, 1, 0]],
                    dtype=np.float32)
    inpt = T.tensor(inpt, dtype=T.float32).to(device)

    log_reg.eval()
    with T.no_grad():
        oupt = log_reg(inpt)  # a Tensor
    pred_prob = oupt.item()  # scalar, [0.0, 1.0]
    print("\nComputed output pp: ", end="")
    print("%0.4f" % pred_prob)

    if pred_prob < 0.5:
        print("Prediction = male")
    else:
        print("Prediction = female")

    print("\nEnd Patient gender demo")


if __name__ == "__main__":
    main()

# -----------------------------------------------------------------

# copy, paste, save as patients_train.txt
# tab-delimited - you might have to replace tabs
# sex (male = 0, female = 1) target
# age (divided by 100)
# county (austin = 1 0 0, bailey = 0 1 0, carson = 0 0 1)
# blood monocyte count
# hospitalization (minor = 1 0 0, moderate = 0 1 0, major = 0 0 1)
#
#	1	0.58	0	1	0	0.654	0	0	1
#	0	0.36	1	0	0	0.445	0	1	0
#	1	0.55	0	0	1	0.646	1	0	0
#	0	0.31	0	1	0	0.464	1	0	0
#	0	0.39	0	0	1	0.512	0	1	0
#	1	0.24	1	0	0	0.295	0	0	1
#	0	0.49	0	1	0	0.667	0	1	0
#	1	0.51	1	0	0	0.561	0	0	1
#	0	0.43	0	0	1	0.532	0	1	0
#	1	0.64	0	0	1	0.711	1	0	0
#	0	0.25	0	0	1	0.371	1	0	0
#	1	0.35	0	0	1	0.352	0	0	1
#	1	0.5	0	1	0	0.565	0	1	0
#	1	0.5	0	0	1	0.55	0	1	0
#	0	0.19	0	0	1	0.327	1	0	0
#	1	0.22	0	1	0	0.277	0	1	0
#	0	0.39	0	0	1	0.471	0	0	1
#	1	0.63	0	1	0	0.758	1	0	0
#	1	0.34	1	0	0	0.394	0	1	0
#	0	0.22	1	0	0	0.335	1	0	0
#	0	0.33	0	1	0	0.464	0	1	0
#	1	0.45	0	1	0	0.541	0	1	0
#	1	0.42	0	1	0	0.507	0	1	0
#	0	0.33	0	1	0	0.468	0	1	0
#	1	0.25	0	0	1	0.3	0	1	0
#	1	0.27	1	0	0	0.325	0	0	1
#	1	0.48	1	0	0	0.54	0	1	0
#	0	0.64	0	1	0	0.713	0	0	1
#	1	0.61	0	1	0	0.724	1	0	0
#	1	0.29	1	0	0	0.363	1	0	0
#	1	0.5	0	0	1	0.55	0	1	0
#	1	0.55	0	0	1	0.625	1	0	0
#	1	0.4	1	0	0	0.524	1	0	0
#	1	0.22	1	0	0	0.236	0	0	1
#	1	0.68	0	1	0	0.784	1	0	0
#	0	0.6	1	0	0	0.717	0	0	1
#	0	0.34	0	0	1	0.465	0	1	0
#	0	0.31	0	1	0	0.489	0	1	0
#	1	0.43	0	0	1	0.48	0	1	0
#	0	0.55	0	1	0	0.607	0	0	1
#	0	0.43	0	1	0	0.511	0	1	0
#	0	0.21	1	0	0	0.372	1	0	0
#	1	0.64	0	1	0	0.748	1	0	0
#	0	0.41	1	0	0	0.588	0	1	0
#	1	0.64	0	0	1	0.727	1	0	0
#	0	0.56	0	0	1	0.666	0	0	1
#	1	0.31	0	0	1	0.36	0	1	0
#	0	0.65	0	0	1	0.701	0	0	1
#	1	0.55	0	0	1	0.643	1	0	0
#	0	0.25	1	0	0	0.403	1	0	0
#	1	0.46	0	0	1	0.51	0	1	0
#	0	0.36	1	0	0	0.535	1	0	0
#	1	0.52	0	1	0	0.581	0	1	0
#	1	0.61	0	0	1	0.679	1	0	0
#	1	0.57	0	0	1	0.657	1	0	0
#	0	0.46	0	1	0	0.526	0	1	0
#	0	0.62	1	0	0	0.668	0	0	1
#	1	0.55	0	0	1	0.627	1	0	0
#	0	0.22	0	0	1	0.277	0	1	0
#	0	0.5	1	0	0	0.629	1	0	0
#	0	0.32	0	1	0	0.418	0	1	0
#	0	0.21	0	0	1	0.356	1	0	0
#	1	0.44	0	1	0	0.52	0	1	0
#	1	0.46	0	1	0	0.517	0	1	0
#	1	0.62	0	1	0	0.697	1	0	0
#	1	0.57	0	1	0	0.664	1	0	0
#	0	0.67	0	0	1	0.758	0	0	1
#	1	0.29	1	0	0	0.343	0	0	1
#	1	0.53	1	0	0	0.601	1	0	0
#	0	0.44	1	0	0	0.548	0	1	0
#	1	0.46	0	1	0	0.523	0	1	0
#	0	0.2	0	1	0	0.301	0	1	0
#	0	0.38	1	0	0	0.535	0	1	0
#	1	0.5	0	1	0	0.586	0	1	0
#	1	0.33	0	1	0	0.425	0	1	0
#	0	0.33	0	1	0	0.393	0	1	0
#	1	0.26	0	1	0	0.404	1	0	0
#	1	0.58	1	0	0	0.707	1	0	0
#	1	0.43	0	0	1	0.48	0	1	0
#	0	0.46	1	0	0	0.644	1	0	0
#	1	0.6	1	0	0	0.717	1	0	0
#	0	0.42	1	0	0	0.489	0	1	0
#	0	0.56	0	0	1	0.564	0	0	1
#	0	0.62	0	1	0	0.663	0	0	1
#	0	0.5	1	0	0	0.648	0	1	0
#	1	0.47	0	0	1	0.52	0	1	0
#	0	0.67	0	1	0	0.804	0	0	1
#	0	0.4	0	0	1	0.504	0	1	0
#	1	0.42	0	1	0	0.484	0	1	0
#	1	0.64	1	0	0	0.72	1	0	0
#	0	0.47	1	0	0	0.587	0	0	1
#	1	0.45	0	1	0	0.528	0	1	0
#	0	0.25	0	0	1	0.409	1	0	0
#	1	0.38	1	0	0	0.484	1	0	0
#	1	0.55	0	0	1	0.6	0	1	0
#	0	0.44	1	0	0	0.606	0	1	0
#	1	0.33	1	0	0	0.41	0	1	0
#	1	0.34	0	0	1	0.39	0	1	0
#	1	0.27	0	1	0	0.337	0	0	1
#	1	0.32	0	1	0	0.407	0	1	0
#	1	0.42	0	0	1	0.47	0	1	0
#	0	0.24	0	0	1	0.403	1	0	0
#	1	0.42	0	1	0	0.503	0	1	0
#	1	0.25	0	0	1	0.28	0	0	1
#	1	0.51	0	1	0	0.58	0	1	0
#	0	0.55	0	1	0	0.635	0	0	1
#	1	0.44	1	0	0	0.478	0	0	1
#	0	0.18	1	0	0	0.398	1	0	0
#	0	0.67	0	1	0	0.716	0	0	1
#	1	0.45	0	0	1	0.5	0	1	0
#	1	0.48	1	0	0	0.558	0	1	0
#	0	0.25	0	1	0	0.39	0	1	0
#	0	0.67	1	0	0	0.783	0	1	0
#	1	0.37	0	0	1	0.42	0	1	0
#	0	0.32	1	0	0	0.427	0	1	0
#	1	0.48	1	0	0	0.57	0	1	0
#	0	0.66	0	0	1	0.75	0	0	1
#	1	0.61	1	0	0	0.7	1	0	0
#	0	0.58	0	0	1	0.689	0	1	0
#	1	0.19	1	0	0	0.24	0	0	1
#	1	0.38	0	0	1	0.43	0	1	0
#	0	0.27	1	0	0	0.364	0	1	0
#	1	0.42	1	0	0	0.48	0	1	0
#	1	0.6	1	0	0	0.713	1	0	0
#	0	0.27	0	0	1	0.348	1	0	0
#	1	0.29	0	1	0	0.371	1	0	0
#	0	0.43	1	0	0	0.567	0	1	0
#	1	0.48	1	0	0	0.567	0	1	0
#	1	0.27	0	0	1	0.294	0	0	1
#	0	0.44	1	0	0	0.552	1	0	0
#	1	0.23	0	1	0	0.263	0	0	1
#	0	0.36	0	1	0	0.53	0	0	1
#	1	0.64	0	0	1	0.725	1	0	0
#	1	0.29	0	0	1	0.3	0	0	1
#	0	0.33	1	0	0	0.493	0	1	0
#	0	0.66	0	1	0	0.75	0	0	1
#	0	0.21	0	0	1	0.343	1	0	0
#	1	0.27	1	0	0	0.327	0	0	1
#	1	0.29	1	0	0	0.318	0	0	1
#	0	0.31	1	0	0	0.486	0	1	0
#	1	0.36	0	0	1	0.41	0	1	0
#	1	0.49	0	1	0	0.557	0	1	0
#	0	0.28	1	0	0	0.384	1	0	0
#	0	0.43	0	0	1	0.566	0	1	0
#	0	0.46	0	1	0	0.588	0	1	0
#	1	0.57	1	0	0	0.698	1	0	0
#	0	0.52	0	0	1	0.594	0	1	0
#	0	0.31	0	0	1	0.435	0	1	0
#	0	0.55	1	0	0	0.62	0	0	1
#	1	0.5	1	0	0	0.564	0	1	0
#	1	0.48	0	1	0	0.559	0	1	0
#	0	0.22	0	0	1	0.345	1	0	0
#	1	0.59	0	0	1	0.667	1	0	0
#	1	0.34	1	0	0	0.428	0	0	1
#	0	0.64	1	0	0	0.772	0	0	1
#	1	0.29	0	0	1	0.335	0	0	1
#	0	0.34	0	1	0	0.432	0	1	0
#	0	0.61	1	0	0	0.75	0	0	1
#	0	0.29	1	0	0	0.413	1	0	0
#	1	0.63	0	1	0	0.706	1	0	0
#	0	0.29	0	1	0	0.4	1	0	0
#	0	0.51	1	0	0	0.627	0	1	0
#	0	0.24	0	0	1	0.377	1	0	0
#	1	0.48	0	1	0	0.575	0	1	0
#	1	0.18	1	0	0	0.274	1	0	0
#	1	0.18	1	0	0	0.203	0	0	1
#	1	0.33	0	1	0	0.382	0	0	1
#	0	0.2	0	0	1	0.348	1	0	0
#	1	0.29	0	0	1	0.33	0	0	1
#	0	0.44	0	0	1	0.63	1	0	0
#	0	0.65	0	0	1	0.818	1	0	0
#	0	0.56	1	0	0	0.637	0	0	1
#	0	0.52	0	0	1	0.584	0	1	0
#	0	0.29	0	1	0	0.486	1	0	0
#	0	0.47	0	1	0	0.589	0	1	0
#	1	0.68	1	0	0	0.726	0	0	1
#	1	0.31	0	0	1	0.36	0	1	0
#	1	0.61	0	1	0	0.625	0	0	1
#	1	0.19	0	1	0	0.215	0	0	1
#	1	0.38	0	0	1	0.43	0	1	0
#	0	0.26	1	0	0	0.423	1	0	0
#	1	0.61	0	1	0	0.674	1	0	0
#	1	0.4	1	0	0	0.465	0	1	0
#	0	0.49	1	0	0	0.652	0	1	0
#	1	0.56	1	0	0	0.675	1	0	0
#	0	0.48	0	1	0	0.66	0	1	0
#	1	0.52	1	0	0	0.563	0	0	1
#	0	0.18	1	0	0	0.298	1	0	0
#	0	0.56	0	0	1	0.593	0	0	1
#	0	0.52	0	1	0	0.644	0	1	0
#	0	0.18	0	1	0	0.286	0	1	0
#	0	0.58	1	0	0	0.662	0	0	1
#	0	0.39	0	1	0	0.551	0	1	0
#	0	0.46	1	0	0	0.629	0	1	0
#	0	0.4	0	1	0	0.462	0	1	0
#	0	0.6	1	0	0	0.727	0	0	1
#	1	0.36	0	1	0	0.407	0	0	1
#	1	0.44	1	0	0	0.523	0	1	0
#	1	0.28	1	0	0	0.313	0	0	1
#	1	0.54	0	0	1	0.626	1	0	0

# -----------------------------------------------------------------

# patients_test.txt
#
# sex (male = 0, female = 1)
# age (divided by 100)
# county (austin = 1 0 0, bailey = 0 1 0, carson = 0 0 1)
# blood monocyte count
# hospitalization (minor = 1 0 0, moderate = 0 1 0, major = 0 0 1)
#
#	1	0.66	0	0	1	0.745	1	0	0
#	0	0.51	1	0	0	0.612	0	1	0
#	1	0.25	0	0	1	0.262	0	0	1
#	0	0.32	0	1	0	0.461	0	1	0
#	1	0.55	1	0	0	0.627	1	0	0
#	1	0.33	0	0	1	0.373	0	0	1
#	0	0.29	0	1	0	0.462	1	0	0
#	1	0.65	1	0	0	0.727	1	0	0
#	0	0.43	0	1	0	0.514	0	1	0
#	0	0.54	0	1	0	0.648	0	0	1
#	1	0.61	0	1	0	0.727	1	0	0
#	1	0.52	0	1	0	0.636	1	0	0
#	1	0.29	1	0	0	0.314	0	0	1
#	0	0.47	0	0	1	0.594	0	1	0
#	1	0.39	0	1	0	0.478	0	1	0
#	1	0.47	0	0	1	0.52	0	1	0
#	0	0.49	1	0	0	0.586	0	1	0
#	0	0.63	0	0	1	0.674	0	0	1
#	0	0.3	1	0	0	0.392	1	0	0
#	0	0.61	0	0	1	0.696	0	0	1
#	0	0.47	0	0	1	0.587	0	1	0
#	1	0.3	0	0	1	0.345	0	0	1
#	0	0.51	0	0	1	0.58	0	1	0
#	0	0.24	1	0	0	0.388	0	1	0
#	0	0.49	1	0	0	0.645	0	1	0
#	1	0.3	0	1	0	0.335	0	0	1
#	0	0.65	1	0	0	0.769	1	0	0
#	0	0.46	0	1	0	0.58	1	0	0
#	0	0.45	0	0	1	0.518	0	1	0
#	0	0.47	1	0	0	0.636	1	0	0
#	0	0.29	1	0	0	0.448	1	0	0
#	0	0.57	0	0	1	0.693	0	0	1
#	0	0.2	1	0	0	0.287	0	0	1
#	0	0.35	1	0	0	0.434	0	1	0
#	0	0.61	0	0	1	0.67	0	0	1
#	0	0.31	0	0	1	0.373	0	1	0
#	1	0.18	1	0	0	0.208	0	0	1
#	1	0.26	0	0	1	0.292	0	0	1
#	0	0.28	1	0	0	0.364	0	0	1
#	0	0.59	0	0	1	0.694	0	0	1
