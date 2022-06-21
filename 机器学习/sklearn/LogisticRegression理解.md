loss函数采用的MSE

对于target要求为continuous，不能是float类型的数据，可以为int型数据

参数coef_的值，如果y里面标签数有3个及以上，coef为二维数组(n_targets, n_features_x)；如果y里面标签为2个，coef为二维数组(只不过只有一行)

对于y里面标签数有3个及以上理解：

![image-20220616100232177](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220616100232177.png)

对多类的这种采用cross-entropy loss

```
class LogisticRegression(LinearClassifierMixin, SparseCoefMixin, BaseEstimator):
tol : float, default=1e-4
        Tolerance for stopping criteria.
max_iter : int, default=100
        Maximum number of iterations taken for the solvers to converge.
```

算法比较

```
- For small datasets, 'liblinear' is a good choice, whereas 'sag'
and 'saga' are faster for large ones;
- For multiclass problems, only 'newton-cg', 'sag', 'saga' and
'lbfgs' handle multinomial loss;
- 'liblinear' is limited to one-versus-rest schemes.
```

然后调用的是_logistic_regression_path(Compute a Logistic Regression model for a list of regularization parameters)

预处理的时候把target处理成为[[1 0 0], [0 1 0], [0 0 1]],w0为[[0. 0. 0.], [0. 0. 0.], [0. 0. 0.]]即把偏移量b直接放在了w中

在_logistic_regression_path, _logistic.py下

```
def func(x, *args):
	return _multinomial_loss_grad(x, *args)[0:2]
```

调用scipy中的

```
opt_res = optimize.minimize(
                func, // 表示损失函数_multinomial_loss_grad
                w0, //[0. 0. 0. 0. 0. 0. 0. 0. 0.]
                method="L-BFGS-B",
                jac=True,
                args=(X, target, 1.0 / C, sample_weight), // target的值[[1 0 0], [0 1 0], [0 0 1]]
                options={"iprint": iprint, "gtol": tol, "maxiter": max_iter},
            )
```

进入到minimize函数

```
def minimize(fun, x0(参数初始值，一维数组), args=()（里面放着数据）, method=None, jac=None（Method for computing the gradient vector，If `jac` is a Boolean and is True, `fun` is 
assumed to return a tuple ``(f, g)`` containing the objective function and the gradient.）, hess=None,
             hessp=None, bounds=None, constraints=(), tol=None,
             callback=None, options=None)
```

```
# fun returns func and grad
fun = MemoizeJac(fun)
jac = fun.derivative
```

然后调用

```
_minimize_lbfgsb(fun, x0（[0. 0. 0. 0. 0. 0. 0. 0. 0.]）, args（X(array([[ 1., -1.],[ 0.,  1.],[ 1.,  1.]]), y array([[1, 0, 0],[0, 1, 0],[0, 0, 1]]), 1.0, array([1., 1., 1.]))）, jac, bounds,
                        callback=callback, **options)
```

```
_minimize_lbfgsb(fun, x0, args=(), jac=None, bounds=None,
                     disp=None, maxcor=10, ftol=2.2204460492503131e-09,
                     gtol=1e-5, eps=1e-8, maxfun=15000, maxiter=15000,
                     iprint=-1, callback=None, maxls=20,
                     finite_diff_rel_step=None, **unknown_options):
```

类ScalarFunction

---

涉及到计算的时候还是用的_logistic.py中的 **_multinomial_loss_grad**

_multinomial_loss_grad里面调用了loss, p（(n_samples, n_classes) Estimated class probabilities）, w = _multinomial_loss(w, X, Y, alpha, sample_weight) Computes multinomial loss and class probabilities.

```
p = safe_sparse_dot(X, w.T)
p += intercept
# p可以理解为预测值矩阵y_pre，整个训练集作为整体
# np.log(np.sum(np.exp(a)))，axis=1表示按行计算
p -= logsumexp(p, axis=1)[:, np.newaxis]
loss = -(sample_weight * Y * p).sum()
# L2正则化
loss += 0.5 * alpha * squared_norm(w)
# 对p矩阵每一个元素都变为exp(value)
p = np.exp(p, p)
# p表示Estimated class probabilities，也可以理解为y_pre
return loss, p, w
```

![image-20220616171818592](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220616171818592.png)

---

```
grad = np.zeros((n_classes, n_features + bool(fit_intercept)), dtype=X.dtype)
loss, p, w = _multinomial_loss(w, X, Y, alpha, sample_weight)
sample_weight = sample_weight[:, np.newaxis]
diff = sample_weight * (p - Y)
grad[:, :n_features] = safe_sparse_dot(diff.T, X)
grad[:, :n_features] += alpha * w
if fit_intercept:
grad[:, -1] = diff.sum(axis=0)
return loss, grad.ravel(), p
```

![image-20220616175030599](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220616175030599.png)

---

在class MemoizeJac中

```
    def _compute_if_needed(self, x, *args):
        if not np.all(x == self.x) or self._value is None or self.jac is None:
            self.x = np.asarray(x).copy()
            fg = self.fun(x, *args) # fg即为loss, grad.ravel(), p
            self.jac = fg[1] # grad.ravel()
            self._value = fg[0] # loss
```

---

在_minimize_lbfgsb, lbfgsb.py:336中

```
x = array(x0, float64) # 未知参数值
f = array(0.0, float64) # loss值
g = zeros((n,), float64) # grad (9,) 
wa = zeros(2*m*n + 5*n + 11*m*m + 8*m, float64) # (1405,) 
iwa = zeros(3*n, fortran_int) # (27,) 
task = zeros(1, 'S60') # [b'']
csave = zeros(1, 'S60') # [b'']
lsave = zeros(4, fortran_int) # [0 0 0 0]
isave = zeros(44, fortran_int) # (44, )
dsave = zeros(29, float64) # (29, )
```

x更新的地方

```
_lbfgsb.setulb(m, x, low_bnd, upper_bnd, nbd, f, g, factr,
                       pgtol, wa, iwa, task, iprint, csave, lsave,
                       isave, dsave, maxls)
```

_lbfgsb.setulb具体实现在.pyd文件中

![image-20220621202744965](https://raw.githubusercontent.com/liang636600/cloudImg/master/images/image-20220621202744965.png)

f与g更新的地方

```
if task_str.startswith(b'FG'):
    # The minimization routine wants f and g at the current x.
    # Note that interruptions due to maxfun are postponed
    # until the completion of the current minimization iteration.
    # Overwrite f and g:
    f, g = func_and_grad(x)
```



