summary(mod_sim_poisson)
x1_predictive=c(0,35,0)
x2_predictive=c(1,35,35)
head(mod_csim_poisson)
loglam1_predictive=mod_csim_poisson[,"int"]+mod_csim_poisson[,c(2,1,3)]%*%x1_predictive
loglam2_predictive=mod_csim_poisson[,"int"]+mod_csim_poisson[,c(2,1,3)]%*%x2_predictive
lam1_predictive=exp(loglam1_predictive)
lam2_predictive=exp(loglam2_predictive)
head(loglam1_predictive)
plot(density(lam1_predictive))
n_sim_predictive=length(lam1_predictive)
y1_predictive=rpois(n_sim_predictive, lam1_predictive)
y2_predictive=rpois(n_sim_predictive, lam2_predictive)

plot(table(factor(y1_predictive, levels=0:18))/n_sim_predictive)
points(table((y2_predictive+.1))/n_sim_predictive, col="red")
mean(y2_predictive>y1_predictive)
