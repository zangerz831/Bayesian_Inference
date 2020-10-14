# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 17:17:47 2020

@author: zachz
"""
import numpy as np
import arviz as az
import scrapy as scrapy
import pandas as pd
from scrapy import Selector
import requests
import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use('seaborn-bright')
from scipy.stats import beta
from scipy.stats import norm
from scipy.stats import binom
import pymc3 as pm
from datetime import datetime


# RUN SCRAPER SCRIPT BEFOREHAND AND GET DATE #
Date = datetime.today().strftime('%m-%d-%Y')

print(usf_hitter_names)

# MODEL #
def bayes_model(player_type, stat, prior_date, todays_date):
   if player_type == 'hitters': 
        date = datetime.today().strftime('%m-%d-%Y')
        team_summary = []
        team_posterior_alphas_betas = []
        prior_df = pd.read_csv("D:\\USF\\Data Frame Time Stamps\\{date}_hitter_df_time_stamp.csv".format(date = prior_date))
        prior_df.rename(columns = {'Unnamed: 0':'Name'}, inplace = True)
        prior_df = prior_df.set_index('Name')
    
        for i in usf_hitter_names:
            if stat == 'OBP':            
                with pm.Model() as model:
                
                    plate_appearances = usf_hitter_data_frame.at['{}'.format(i), 'PA'] - prior_df.at['{}'.format(i), 'PA']
                    if plate_appearances == 0: plate_appearances = usf_hitter_data_frame.at['{}'.format(i), 'PA']
                    events = usf_hitter_data_frame.at['{}'.format(i), 'PA']*usf_hitter_data_frame.at['{}'.format(i), 'OB%'] - (prior_df.at['{}'.format(i), 'PA']*prior_df.at['{}'.format(i), 'OB%'])
                    p = pm.Beta("p", alpha = hitters_obp_priors.at['{}'.format(i), 'Alpha'], beta = hitters_obp_priors.at['{}'.format(i), 'Beta'])
                    likelihood = pm.Binomial("likelihood", 
                                             p = p,
                                             n = plate_appearances,
                                             observed = events)

                with model:
                    trace_pa = pm.sample(1000, tune = 1000, cores = 1)
                    pm.plot_posterior(trace_pa)
                    posterior_alphas_betas = pd.DataFrame({'Name': [i],
                                                           'Alpha': [hitters_obp_priors.at['{}'.format(i), 'Alpha'] + events], 
                                                           'Beta': [(hitters_obp_priors.at['{}'.format(i), 'Beta']) + (plate_appearances - events)],
                                                           'Stat': [stat],
                                                           'Date': [date]})    
                    posterior_alphas_betas.set_index('Name')
                    player_summary = pm.summary(trace_pa)
                    player_summary['player'] = i
                    player_summary.drop(columns = ['mcse_mean', 'mcse_sd', 'ess_mean', 'ess_sd', 'ess_bulk', 'ess_tail', 'r_hat'])
    
    
                    team_summary.append(player_summary)
                    team_posterior_alphas_betas.append(posterior_alphas_betas)
        
        
            elif stat == 'K':
                with pm.Model() as model:
                    plate_appearances = usf_hitter_data_frame.at['{}'.format(i), 'PA'] - prior_df.at['{}'.format(i), 'PA']
                    if plate_appearances == 0: plate_appearances = usf_hitter_data_frame.at['{}'.format(i), 'PA']
                    events = usf_hitter_data_frame.at['{}'.format(i), 'SO']
                    p = pm.Beta("p", alpha = hitters_k_priors.at['{}'.format(i), 'Alpha'], beta = hitters_k_priors.at['{}'.format(i), 'Beta'])
                    likelihood = pm.Binomial("likelihood", 
                                             p = p,
                                             n = plate_appearances,
                                             observed = events)

                with model:
                    trace_pa = pm.sample(1000, tune = 1000, cores = 1)
                    pm.plot_posterior(trace_pa)
                    posterior_alphas_betas = pd.DataFrame({'Name': [i],
                                                           'Alpha': [hitters_k_priors.at['{}'.format(i), 'Alpha'] + events], 
                                                           'Beta': [(hitters_k_priors.at['{}'.format(i), 'Beta']) + (plate_appearances - events)],
                                                           'Stat': [stat],
                                                           'Date': [date]})    
                    posterior_alphas_betas.set_index('Name')
                    player_summary = pm.summary(trace_pa)
                    player_summary['player'] = i
                    player_summary.drop(columns = ['mcse_mean', 'mcse_sd', 'ess_mean', 'ess_sd', 'ess_bulk', 'ess_tail', 'r_hat'])
    
    
                    team_summary.append(player_summary)
                    team_posterior_alphas_betas.append(posterior_alphas_betas)
    
        
            elif stat == 'Damage':
                with pm.Model() as model:
                    plate_appearances = usf_hitter_data_frame.at['{}'.format(i), 'PA'] - prior_df.at['{}'.format(i), 'PA']
                    if plate_appearances == 0: plate_appearances = usf_hitter_data_frame.at['{}'.format(i), 'PA']
                    events = usf_hitter_data_frame.at['{}'.format(i), 'DAMAGE']
                    p = pm.Beta("p", alpha = hitters_damage_priors.at['{}'.format(i), 'Alpha'], beta = hitters_damage_priors.at['{}'.format(i), 'Beta'])
                    likelihood = pm.Binomial("likelihood", 
                                             p = p,
                                             n = plate_appearances,
                                             observed = events)

                with model:
                    trace_pa = pm.sample(1000, tune = 1000, cores = 1)
                    pm.plot_posterior(trace_pa)
                    posterior_alphas_betas = pd.DataFrame({'Name': [i],
                                                           'Alpha': [hitters_k_priors.at['{}'.format(i), 'Alpha'] + events], 
                                                           'Beta': [(hitters_k_priors.at['{}'.format(i), 'Beta']) + (plate_appearances - events)],
                                                           'Stat': [stat],
                                                           'Date': [date]})    
                    posterior_alphas_betas.set_index('Name')
                    player_summary = pm.summary(trace_pa)
                    player_summary['player'] = i
                    player_summary.drop(columns = ['mcse_mean', 'mcse_sd', 'ess_mean', 'ess_sd', 'ess_bulk', 'ess_tail', 'r_hat'])
    
    
                    team_summary.append(player_summary)
                    team_posterior_alphas_betas.append(posterior_alphas_betas)
    
        team_posterior_alphas_betas = pd.concat(team_posterior_alphas_betas)
        team_summary = pd.concat(team_summary)
        outPath_posterior_alphas_betas = "D:\\USF\\Posteriors\\{}\\{}\\{} {} Posterior Alphas and Betas.csv".format(player_type,stat, date, stat)
        team_posterior_alphas_betas.to_csv(outPath_posterior_alphas_betas)
        outPath_posterior_summary = "D:\\USF\\Posteriors\\{}\\{}\\{} {} Posterior Summary.csv".format(player_type, stat, date, stat)
        team_summary.to_csv(outPath_posterior_summary)
    
   elif player_type == 'pitchers':
        date = datetime.today().strftime('%m-%d-%Y')
        team_summary = []
        team_posterior_alphas_betas = []
        prior_df = pd.read_csv("D:\\USF\\Data Frame Time Stamps\\{date}_pitcher_df_time_stamp.csv".format(date = prior_date))
        prior_df.rename(columns = {'Unnamed: 0':'Name'}, inplace = True)
        prior_df = prior_df.set_index('Name')
        

        for i in usf_pitcher_names:
                if stat == 'OBP':            
                    with pm.Model() as model:
                        batters_faced = usf_pitcher_data_frame.at['{}'.format(i), 'BF'] - prior_df.at['{}'.format(i), 'BF']
                        if batters_faced == 0: batters_faced = usf_pitcher_data_frame.at['{}'.format(i), 'BF']
                        events = usf_pitcher_data_frame.at['{}'.format(i), 'BF']*usf_pitcher_data_frame.at['{}'.format(i), 'OB%'] - (prior_df.at['{}'.format(i), 'BF']*prior_df.at['{}'.format(i), 'OB%'])
                        p = pm.Beta("p", alpha = pitcher_obp_priors.at['{}'.format(i), 'Alpha'], beta = pitcher_obp_priors.at['{}'.format(i), 'Beta'])
                        likelihood = pm.Binomial("likelihood", 
                                                 p = p,
                                                 n = batters_faced,
                                                 observed = events)

                    with model:
                        trace_pa = pm.sample(1000, tune = 1000, cores = 1)
                        pm.plot_posterior(trace_pa)
                        posterior_alphas_betas = pd.DataFrame({'Name': [i],
                                                               'Alpha': [pitcher_obp_priors.at['{}'.format(i), 'Alpha'] + events], 
                                                               'Beta': [(pitcher_obp_priors.at['{}'.format(i), 'Beta']) + (batters_faced - events)],
                                                               'Stat': [stat],
                                                               'Date': [date]})    
                        posterior_alphas_betas.set_index('Name')
                        player_summary = pm.summary(trace_pa)
                        player_summary['player'] = i
                        player_summary.drop(columns = ['mcse_mean', 'mcse_sd', 'ess_mean', 'ess_sd', 'ess_bulk', 'ess_tail', 'r_hat'])
    
    
                        team_summary.append(player_summary)
                        team_posterior_alphas_betas.append(posterior_alphas_betas)
        
        
                elif stat == 'K':
                    with pm.Model() as model:
                        batters_faced = usf_pitcher_data_frame.at['{}'.format(i), 'BF'] - prior_df.at['{}'.format(i), 'BF']
                        if batters_faced == 0: batters_faced = usf_pitcher_data_frame.at['{}'.format(i), 'BF']
                        events = usf_pitcher_data_frame.at['{}'.format(i), 'SO']
                        p = pm.Beta("p", alpha = pitcher_k_priors.at['{}'.format(i), 'Alpha'], beta = pitcher_k_priors.at['{}'.format(i), 'Beta'])
                        likelihood = pm.Binomial("likelihood", 
                                                 p = p,
                                                 n = batters_faced,
                                                 observed = events)

                    with model:
                        trace_pa = pm.sample(1000, tune = 1000, cores = 1)
                        pm.plot_posterior(trace_pa)
                        posterior_alphas_betas = pd.DataFrame({'Name': [i],
                                                               'Alpha': [pitcher_k_priors.at['{}'.format(i), 'Alpha'] + events], 
                                                               'Beta': [(pitcher_k_priors.at['{}'.format(i), 'Beta']) + (batters_faced - events)],
                                                               'Stat': [stat],
                                                               'Date': [date]})    
                        posterior_alphas_betas.set_index('Name')
                        player_summary = pm.summary(trace_pa)
                        player_summary['player'] = i
                        player_summary.drop(columns = ['mcse_mean', 'mcse_sd', 'ess_mean', 'ess_sd', 'ess_bulk', 'ess_tail', 'r_hat'])
    
                        team_summary.append(player_summary)
                        team_posterior_alphas_betas.append(posterior_alphas_betas)

        
                elif stat == 'BB':
                    with pm.Model() as model:
                        batters_faced = usf_pitcher_data_frame.at['{}'.format(i), 'BF'] - prior_df.at['{}'.format(i), 'BF']
                        if batters_faced == 0: batters_faced = usf_pitcher_data_frame.at['{}'.format(i), 'BF']
                        events = usf_pitcher_data_frame.at['{}'.format(i), 'BB']
                        p = pm.Beta("p", alpha = pitcher_bb_priors.at['{}'.format(i), 'Alpha'], beta = pitcher_bb_priors.at['{}'.format(i), 'Beta'])
                        likelihood = pm.Binomial("likelihood", 
                                                 p = p,
                                                 n = batters_faced,
                                                 observed = events)

                    with model:
                        trace_pa = pm.sample(1000, tune = 1000, cores = 1)
                        pm.plot_posterior(trace_pa)
                        posterior_alphas_betas = pd.DataFrame({'Name': [i],
                                                               'Alpha': [pitcher_bb_priors.at['{}'.format(i), 'Alpha'] + events], 
                                                               'Beta': [(pitcher_bb_priors.at['{}'.format(i), 'Beta']) + (batters_faced - events)],
                                                               'Stat': [stat],
                                                               'Date': [date]})    
                        posterior_alphas_betas.set_index('Name')
                        player_summary = pm.summary(trace_pa)
                        player_summary['player'] = i
                        player_summary.drop(columns = ['mcse_mean', 'mcse_sd', 'ess_mean', 'ess_sd', 'ess_bulk', 'ess_tail', 'r_hat'])
    
    
                        team_summary.append(player_summary)
                        team_posterior_alphas_betas.append(posterior_alphas_betas)
    
        team_posterior_alphas_betas = pd.concat(team_posterior_alphas_betas)
        team_summary = pd.concat(team_summary)
        outPath_posterior_alphas_betas = "D:\\USF\\Posteriors\\{}\\{}\\{} {} Posterior Alphas and Betas.csv".format(player_type, stat, date, stat)
        team_posterior_alphas_betas.to_csv(outPath_posterior_alphas_betas)
        outPath_posterior_summary = "D:\\USF\\Posteriors\\{}\\{}\\{} {} Posterior Summary.csv".format(player_type, stat, date, stat)
        team_summary.to_csv(outPath_posterior_summary)




def bayes_model_2(player_type, stat,todays_date):
   if player_type == 'hitters': 
        date = datetime.today().strftime('%m-%d-%Y')
        team_summary = []
        team_posterior_alphas_betas = []
        prior_df = pd.read_csv("D:\\USF\\Data Frame Time Stamps\\{date}_hitter_df_time_stamp.csv".format(date = prior_date))
        prior_df.rename(columns = {'Unnamed: 0':'Name'}, inplace = True)
        prior_df = prior_df.set_index('Name')
    
        for i in usf_hitter_names:
            if stat == 'OBP':            
                with pm.Model() as model:
                
                    plate_appearances = usf_hitter_data_frame.at['{}'.format(i), 'PA'] - prior_df.at['{}'.format(i), 'PA']
                    if plate_appearances == 0: plate_appearances = usf_hitter_data_frame.at['{}'.format(i), 'PA']
                    events = usf_hitter_data_frame.at['{}'.format(i), 'PA']*usf_hitter_data_frame.at['{}'.format(i), 'OB%'] - (prior_df.at['{}'.format(i), 'PA']*prior_df.at['{}'.format(i), 'OB%'])
                    p = pm.Beta("p", alpha = hitters_obp_priors.at['{}'.format(i), 'Alpha'], beta = hitters_obp_priors.at['{}'.format(i), 'Beta'])
                    likelihood = pm.Binomial("likelihood", 
                                             p = p,
                                             n = plate_appearances,
                                             observed = events)

                with model:
                    trace_pa = pm.sample(1000, tune = 1000, cores = 1)
                    pm.plot_posterior(trace_pa)
                    posterior_alphas_betas = pd.DataFrame({'Name': [i],
                                                           'Alpha': [hitters_obp_priors.at['{}'.format(i), 'Alpha'] + events], 
                                                           'Beta': [(hitters_obp_priors.at['{}'.format(i), 'Beta']) + (plate_appearances - events)],
                                                           'Stat': [stat],
                                                           'Date': [date]})    
                    posterior_alphas_betas.set_index('Name')
                    player_summary = pm.summary(trace_pa)
                    player_summary['player'] = i
                    player_summary.drop(columns = ['mcse_mean', 'mcse_sd', 'ess_mean', 'ess_sd', 'ess_bulk', 'ess_tail', 'r_hat'])
    
    
                    team_summary.append(player_summary)
                    team_posterior_alphas_betas.append(posterior_alphas_betas)
        
        
            elif stat == 'K':
                with pm.Model() as model:
                    plate_appearances = usf_hitter_data_frame.at['{}'.format(i), 'PA'] - prior_df.at['{}'.format(i), 'PA']
                    if plate_appearances == 0: plate_appearances = usf_hitter_data_frame.at['{}'.format(i), 'PA']
                    events = usf_hitter_data_frame.at['{}'.format(i), 'SO']
                    p = pm.Beta("p", alpha = hitters_k_priors.at['{}'.format(i), 'Alpha'], beta = hitters_k_priors.at['{}'.format(i), 'Beta'])
                    likelihood = pm.Binomial("likelihood", 
                                             p = p,
                                             n = plate_appearances,
                                             observed = events)

                with model:
                    trace_pa = pm.sample(1000, tune = 1000, cores = 1)
                    pm.plot_posterior(trace_pa)
                    posterior_alphas_betas = pd.DataFrame({'Name': [i],
                                                           'Alpha': [hitters_k_priors.at['{}'.format(i), 'Alpha'] + events], 
                                                           'Beta': [(hitters_k_priors.at['{}'.format(i), 'Beta']) + (plate_appearances - events)],
                                                           'Stat': [stat],
                                                           'Date': [date]})    
                    posterior_alphas_betas.set_index('Name')
                    player_summary = pm.summary(trace_pa)
                    player_summary['player'] = i
                    player_summary.drop(columns = ['mcse_mean', 'mcse_sd', 'ess_mean', 'ess_sd', 'ess_bulk', 'ess_tail', 'r_hat'])
    
    
                    team_summary.append(player_summary)
                    team_posterior_alphas_betas.append(posterior_alphas_betas)
    
        
            elif stat == 'Damage':
                with pm.Model() as model:
                    plate_appearances = usf_hitter_data_frame.at['{}'.format(i), 'PA'] - prior_df.at['{}'.format(i), 'PA']
                    if plate_appearances == 0: plate_appearances = usf_hitter_data_frame.at['{}'.format(i), 'PA']
                    events = usf_hitter_data_frame.at['{}'.format(i), 'DAMAGE']
                    p = pm.Beta("p", alpha = hitters_damage_priors.at['{}'.format(i), 'Alpha'], beta = hitters_damage_priors.at['{}'.format(i), 'Beta'])
                    likelihood = pm.Binomial("likelihood", 
                                             p = p,
                                             n = plate_appearances,
                                             observed = events)

                with model:
                    trace_pa = pm.sample(1000, tune = 1000, cores = 1)
                    pm.plot_posterior(trace_pa)
                    posterior_alphas_betas = pd.DataFrame({'Name': [i],
                                                           'Alpha': [hitters_k_priors.at['{}'.format(i), 'Alpha'] + events], 
                                                           'Beta': [(hitters_k_priors.at['{}'.format(i), 'Beta']) + (plate_appearances - events)],
                                                           'Stat': [stat],
                                                           'Date': [date]})    
                    posterior_alphas_betas.set_index('Name')
                    player_summary = pm.summary(trace_pa)
                    player_summary['player'] = i
                    player_summary.drop(columns = ['mcse_mean', 'mcse_sd', 'ess_mean', 'ess_sd', 'ess_bulk', 'ess_tail', 'r_hat'])
    
    
                    team_summary.append(player_summary)
                    team_posterior_alphas_betas.append(posterior_alphas_betas)
    
        team_posterior_alphas_betas = pd.concat(team_posterior_alphas_betas)
        team_summary = pd.concat(team_summary)
        outPath_posterior_alphas_betas = "D:\\USF\\Posteriors\\{}\\{}\\{} {} Posterior Alphas and Betas.csv".format(player_type,stat, date, stat)
        team_posterior_alphas_betas.to_csv(outPath_posterior_alphas_betas)
        outPath_posterior_summary = "D:\\USF\\Posteriors\\{}\\{}\\{} {} Posterior Summary.csv".format(player_type, stat, date, stat)
        team_summary.to_csv(outPath_posterior_summary)
    
   elif player_type == 'pitchers':
        date = datetime.today().strftime('%m-%d-%Y')
        team_summary = []
        team_posterior_alphas_betas = []
        

        for i in usf_pitcher_names:
                if stat == 'OBP':            
                    with pm.Model() as model:
                        batters_faced = usf_pitcher_data_frame.at['{}'.format(i), 'BF']
                        events = usf_pitcher_data_frame.at['{}'.format(i), 'BF']*usf_pitcher_data_frame.at['{}'.format(i), 'OB%']
                        p = pm.Beta("p", alpha = pitcher_obp_priors.at['{}'.format(i), 'Alpha'], beta = pitcher_obp_priors.at['{}'.format(i), 'Beta'])
                        likelihood = pm.Binomial("likelihood", 
                                                 p = p,
                                                 n = batters_faced,
                                                 observed = events)

                    with model:
                        trace_pa = pm.sample(1000, tune = 1000, cores = 1)
                        pm.plot_posterior(trace_pa)
                        posterior_alphas_betas = pd.DataFrame({'Name': [i],
                                                               'Alpha': [pitcher_obp_priors.at['{}'.format(i), 'Alpha'] + events], 
                                                               'Beta': [(pitcher_obp_priors.at['{}'.format(i), 'Beta']) + (batters_faced - events)],
                                                               'Stat': [stat],
                                                               'Date': [date]})    
                        posterior_alphas_betas.set_index('Name')
                        player_summary = pm.summary(trace_pa)
                        player_summary['player'] = i
                        player_summary.drop(columns = ['mcse_mean', 'mcse_sd', 'ess_mean', 'ess_sd', 'ess_bulk', 'ess_tail', 'r_hat'])
    
    
                        team_summary.append(player_summary)
                        team_posterior_alphas_betas.append(posterior_alphas_betas)
        
        
                elif stat == 'K':
                    with pm.Model() as model:
                        batters_faced = usf_pitcher_data_frame.at['{}'.format(i), 'BF']
                        events = usf_pitcher_data_frame.at['{}'.format(i), 'SO']
                        p = pm.Beta("p", alpha = pitcher_k_priors.at['{}'.format(i), 'Alpha'], beta = pitcher_k_priors.at['{}'.format(i), 'Beta'])
                        likelihood = pm.Binomial("likelihood", 
                                                 p = p,
                                                 n = batters_faced,
                                                 observed = events)

                    with model:
                        trace_pa = pm.sample(1000, tune = 1000, cores = 1)
                        pm.plot_posterior(trace_pa)
                        posterior_alphas_betas = pd.DataFrame({'Name': [i],
                                                               'Alpha': [pitcher_k_priors.at['{}'.format(i), 'Alpha'] + events], 
                                                               'Beta': [(pitcher_k_priors.at['{}'.format(i), 'Beta']) + (batters_faced - events)],
                                                               'Stat': [stat],
                                                               'Date': [date]})    
                        posterior_alphas_betas.set_index('Name')
                        player_summary = pm.summary(trace_pa)
                        player_summary['player'] = i
                        player_summary.drop(columns = ['mcse_mean', 'mcse_sd', 'ess_mean', 'ess_sd', 'ess_bulk', 'ess_tail', 'r_hat'])
    
                        team_summary.append(player_summary)
                        team_posterior_alphas_betas.append(posterior_alphas_betas)

        
                elif stat == 'BB':
                    with pm.Model() as model:
                        batters_faced = usf_pitcher_data_frame.at['{}'.format(i), 'BF']
                        events = usf_pitcher_data_frame.at['{}'.format(i), 'BB']
                        p = pm.Beta("p", alpha = pitcher_bb_priors.at['{}'.format(i), 'Alpha'], beta = pitcher_bb_priors.at['{}'.format(i), 'Beta'])
                        likelihood = pm.Binomial("likelihood", 
                                                 p = p,
                                                 n = batters_faced,
                                                 observed = events)

                    with model:
                        trace_pa = pm.sample(1000, tune = 1000, cores = 1)
                        pm.plot_posterior(trace_pa)
                        posterior_alphas_betas = pd.DataFrame({'Name': [i],
                                                               'Alpha': [pitcher_bb_priors.at['{}'.format(i), 'Alpha'] + events], 
                                                               'Beta': [(pitcher_bb_priors.at['{}'.format(i), 'Beta']) + (batters_faced - events)],
                                                               'Stat': [stat],
                                                               'Date': [date]})    
                        posterior_alphas_betas.set_index('Name')
                        player_summary = pm.summary(trace_pa)
                        player_summary['player'] = i
                        player_summary.drop(columns = ['mcse_mean', 'mcse_sd', 'ess_mean', 'ess_sd', 'ess_bulk', 'ess_tail', 'r_hat'])
    
    
                        team_summary.append(player_summary)
                        team_posterior_alphas_betas.append(posterior_alphas_betas)
    
        team_posterior_alphas_betas = pd.concat(team_posterior_alphas_betas)
        team_summary = pd.concat(team_summary)
        outPath_posterior_alphas_betas = "D:\\USF\\Posteriors\\{}\\{}\\{} {} Posterior Alphas and Betas.csv".format(player_type, stat, date, stat)
        team_posterior_alphas_betas.to_csv(outPath_posterior_alphas_betas)
        outPath_posterior_summary = "D:\\USF\\Posteriors\\{}\\{}\\{} {} Posterior Summary.csv".format(player_type, stat, date, stat)
        team_summary.to_csv(outPath_posterior_summary)
bayes_model_2('pitchers', 'OBP', '03-11-2020')
bayes_model_2('pitchers', 'K', '03-11-2020')
bayes_model_2('pitchers', 'BB', '03-11-2020')