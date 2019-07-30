library(dplyr)
library(rjags)
summary(cape_cod_batters %>%
       filter(PA>100) %>%
       select(OBP))
sqrt(var(cape_cod_batters %>%
  filter(PA>100) %>%
  select(OBP)))


nn_model <- "model{
    # Likelihood model for Y[i]
for(i in 1:length(Y)) {
Y[i] ~ dnorm(m,s^(-2))
}


m ~ dnorm(.347,.048^(-2))
s ~ dunif(0,.048)
}"

nn_jags <- jags.model(
  textConnection(nn_model),
  data = list(Y = (cape_cod_batters %>%
                     filter(PA>100))$OBP),
  inits = list(.RNG.name = "base::Wichmann-Hill", .RNG.seed = 1989)
)

nn_sim <- coda.samples(model = nn_jags, variable.names = c("m", "s"), n.iter = 10000)

plot(nn_sim)