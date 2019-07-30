library(dplyr)
library(rjags)
library(ggplot2)
mean(wcc_team_offense$OBP)
mean((wcc_hitters %>%
        filter(PA>100))$OBP)

###MODEL###
bin_model <- "model{
    # Likelihood model for X
X ~ dbin(p, n)

# Prior model for p
p ~ dbeta(a, b)
}"

# COMPILE the model    
bin_jags <- jags.model(textConnection(bin_model), 
                        data = list(a = 12, b = 227, X = 7, n = 71),
                        inits = list(.RNG.name = "base::Wichmann-Hill", .RNG.seed = 100))

# SIMULATE the posterior
bin_sim <- coda.samples(model = bin_jags, variable.names = c("p"), n.iter = 10000)

# PLOT the posterior
plot(bin_sim, trace = FALSE)


##NORMAL_NORMAL_WORK##
rnorm(10,50,25)

mean((wcc_hitters %>%
        filter(PA>100))$OBP)

sd((wcc_hitters %>%
        filter(PA>100))$OBP)

rnorm(100,.354,.056)
runif(100, 0, .100)



nn_model <- "model{
    # Likelihood model for Y[i]
for(i in 1:length(Y)) {
Y[i] ~ dnorm(m,s^(-2))
}

# Prior models for m and s
m ~ dnorm(.354,.056^(-2))
s ~ dunif(0,.056)
}"

nn_jags <- jags.model(
  textConnection(nn_model),
  data = list(Y = (wcc_hitters %>%
                     filter(PA>100))$OBP),
  inits = list(.RNG.name = "base::Wichmann-Hill", .RNG.seed = 1989)
)

nn_sim <- coda.samples(model = nn_jags, variable.names = c("m", "s"), n.iter = 10000)

plot(nn_sim, trace = TRUE)

plot(bin_sim, trace = FALSE)

rbeta(n=10000, shape1=45, shape2=55)