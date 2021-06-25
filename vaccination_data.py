# import requests
from datetime import timedelta, datetime
import pandas as pd
import matplotlib.pyplot as plt
# import streamlit as st
 
def main():
    src_url = 'https://github.com/owid/covid-19-data/blob/master/public/data/vaccinations/vaccinations.csv'
    src_ind_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/country_data/India.csv'

    # Create dataframe from web URL data
    df = pd.read_csv(src_ind_url)
    df['daily_d1'] = df['people_vaccinated'].diff()
    df0 = df.set_index('date')
    print(df0.tail())
    
    # define date parameters
    latest_date = df['date'].iloc[-1]
    latest_date_obj = datetime.strptime(latest_date, '%Y-%m-%d')
    last_date_disp = latest_date_obj.strftime('%d %B %Y')
    deadline = '2021-12-31'
    deadline_obj = datetime.strptime(deadline, '%Y-%m-%d')
    deadline_disp = deadline_obj.strftime('%d %B %Y')
    duration = (deadline_obj - latest_date_obj).days
    dt_range = pd.period_range(start=latest_date_obj+pd.Timedelta(1, unit='D'), end=deadline)
    dts = dt_range.strftime('%Y-%m-%d')
    
    # assign values to variables and calculate rates
    single_so_far = df['people_vaccinated'].iloc[-1]
    full_so_far = df['people_fully_vaccinated'].iloc[-1]
    target_population = 1000000000
    balance_population = target_population - single_so_far
    rvr = round(balance_population / duration)  # required vaccination rate
    block = 10  # set of days to caluculate the current rate from
    cvr = round(df['daily_d1'].tail(block).mean()) # current vaccination rate

    # calculate forecast numbers
    max_till_now = df['daily_d1'].max()
    max_possible = single_so_far + cvr * duration
    trail = target_population - max_possible
    balance_days = round(balance_population / cvr)
    new_deadline_obj = latest_date_obj + timedelta(days=balance_days)
    new_deadline_disp = datetime.strftime(new_deadline_obj, '%d %B %Y')
    projection = [(single_so_far + period*cvr) for period in range(1,len(dts)+1)] 
    df_proj_s = pd.Series(projection, index=dts, name='projected_d1')
    df_proj_df = df_proj_s.to_frame()
    df2 = df0.append(df_proj_df)
    print(df2.tail())
    
    # Display information on screen
    print(f'India COVID Vaccination Summary until {last_date_disp}')
    print(f'Vaccinated {single_so_far:,} out of {target_population:,} with only single dose.')
    print(f'Need {balance_population:,} in {duration} days until {deadline_disp} @ {rvr:,} per day.')
    print(f'Current vaccination rate (last {block} days average): {cvr:,} per day.')
    print(f'May get only {max_possible:,} and will trail by {trail:,}.')
    print(f'May reach target population by {new_deadline_disp} at this rate.')

    story_count = 179172948
    story_cvr = 2566157
    story_rvr = 3931919

    print("Namaskar, I made my first video on COVID vaccination trend in India on 29 May more as a need of the hour that I felt from within to perceive and then mathematically analyse the situation of vaccination in our country myself and share the views with others. Subsequently I wrote a story on Medium.com a week later to follow that up with some revised and more practical figures. I have provided the links to both of the efforts in the description. Please go through them if you are interested.")
    print("https://youtu.be/JomMd0nvm2k")
    print("https://parijatprasun.medium.com/covid-vaccination-in-india-are-we-on-track-8198c5e516c9")
    print("It has been almost a month since the video was published and in this one month the scenario has changed a lot, which is, for a change, pretty positive. In this story we'll try to assess the emerged situation.")
    print("First of all, let's pay attention to a very special day in this said period, 21 June, which is International Yoga Day. And what is the connection of International Yoga Day with the course of COVID vaccination? I don't know. Nevertheless, that was the special day that was chosen to bring up some long-awaited changes in the country's vaccination policy and that's the reason this day has become significant for us in this assessment.")
    print(f"On 21 June India recorded a humungous number of {int(max_till_now):,} vaccinations of only first dose administered in a single day. This is definitely an achievement, and a moment of pride and hope for every single one of us beyond doubt.")
    print(f"We saw celebratory statements and posts everywhere, which is not bad. No wonder some of the statements became haughty disregarding facts. I have complete faith in the Co-WIN system judging by its overall operational design and transparency observed so far. Our whole analysis is based on data from Co-WIN dashboard, so there is no scope of doubt about the correctness of the figures, at least till now. Surprisingly, the Co-WIN dashboard itself shows some abnormal figures in the days preceding the special day with respect to some specific states in India which will certainly raise a few questions in the minds of people who rely on information rather than perception about how such a high number could be achieved in a single day. Anyway, let's not get into that discussion. On the whole, we are quite happy about the numbers because at the end of the day, it's for our own benefit.")
    print(f"While writing this story the number of vaccinated people with at least one dose till {last_date_disp} is {single_so_far:,}, increased by about {(single_so_far-story_count):,} since the last count in my follow-up story published on 6 June that was {story_count:,}.")
    print('<Show plot 1>')
    print(f"Based on the revision I incorporated in my follow-up story, the current rate of vaccination (CVR) as of now is {cvr:,} which is calculated taking an average of last {block} days' counts. During my story it was around {story_cvr:,}.")
    print('<Show plot 2>')
    print(f"This Manhattan plot shows the drastic increase in the rate thanks to the International Yoga Day accomplishment that is standing tall like the statue of unity amongst other high-rises.") 
    print(f"The analogy with cricket is inevitable. On one hand, we can see the asking rate or required vaccination rate (RVR) has in fact gone up from {story_rvr:,} in my story to {rvr:,}, but on the other hand, the encouraging thing is that the CVR is currently higher than the RVR! Yay! At this rate we will not only complete vaccinatation of our target figure of {target_population:,} people, we will do it by {new_deadline_disp} well within our target date. And by {deadline_disp} we'll be able to surpass the target and reach around {max_possible:,}. Bravo!, or rather Bravi! The more the better. The sooner the better.")
    print('<show plot3>')
    print(f"Now we have to ensure that we have enough supply and proper distribution of vaccines so we can maintain this rate in the coming days. We'd rather be ravenously hopeful that there will be a few more special days like the last one in a short time. We'll now have to think of administering the second dose as well within the shortest time possible. We're all rooting for that, badly, because the number of people with full vaccination is still lurking around only {full_so_far:,}. This is being deprived of the importance it deserves. Because 'No one is safe, until everyone is.' Thanks for reading.")
    print("I'd love to hear from you about your thoughts, feelings, views on this topic through your claps, likes, and comments at the following places -")
    print("twitter.com/parijatprasun")
    print("facebook.com/parijatprasun")

    # Prepare additional data for plotting
    df0 = df.set_index('date')
    df0['cvr'] = cvr
    df0['rvr'] = rvr
    font_name = 'Open Sans'

    # Plot the data
    fig1 = plt.figure(figsize=(21,9), dpi=150, facecolor=None, edgecolor=None, frameon=False)
    plt.plot(df0['people_vaccinated'], label='People vaccinated with one dose')
    plt.plot(df0['people_fully_vaccinated'], label='People vaccinated with two doses')
    plt.title('India Vaccination Trend', loc='left', fontname=font_name, fontsize=40, fontweight='bold')
    plt.xlabel('Days', fontname=font_name, fontsize=28, fontweight='bold')
    plt.ylabel('Population', fontname=font_name, fontsize=28, fontweight='bold')
    plt.xticks(fontname=font_name, fontsize=10, rotation='vertical')
    plt.yticks(fontname=font_name, fontsize=20)
    plt.ticklabel_format(axis='y', style='plain', scilimits=None, useOffset=None)
    plt.annotate(f'{single_so_far:,}', xy=('2021-05-30', 240000000), fontname=font_name, fontsize=32)
    plt.annotate(f'{full_so_far:,}', xy=('2021-06-10', 55000000), fontname=font_name, fontsize=20)
    plt.tight_layout()
    # plt.legend(loc=9)
    plt.legend(loc=2, prop={'family':font_name, 'size':20})
    plt.savefig('plot1.png')
    # plt.show()

    fig2 = plt.figure(figsize=(21,9), dpi=150, facecolor=None, edgecolor=None, frameon=False)
    plt.bar(df0.index, df0['daily_d1'], color='orange', label='Daily vaccination count')
    plt.plot(df0['cvr'], color='green', label='CVR')
    plt.plot(df0['rvr'], color='red', label='RVR') 
    plt.title('India Vaccination Trend', loc='left', fontname=font_name, fontsize=40, fontweight='bold')
    plt.xlabel('Days', fontname=font_name, fontsize=28, fontweight='bold')
    plt.ylabel('Population', fontname=font_name, fontsize=28, fontweight='bold')
    plt.xticks(fontname=font_name, fontsize=10, rotation='vertical')
    plt.yticks(fontname=font_name, fontsize=20)
    plt.ticklabel_format(axis='y', style='plain', scilimits=None, useOffset=None)
    plt.annotate(f'{cvr:,}', xy=('2021-04-30', 4500000), fontname=font_name, fontsize=32)
    plt.annotate(f'{rvr:,}', xy=('2021-04-30', 3300000), fontname=font_name, fontsize=32)
    plt.annotate(f'{int(max_till_now):,}', xy=('2021-06-21', 8200000), xytext=('2021-05-25', 8200000), arrowprops=dict(arrowstyle="->", connectionstyle="arc3"), fontname=font_name, fontsize=20)
    plt.tight_layout()
    # plt.legend(loc=9)
    plt.legend(loc=2, prop={'family':font_name, 'size':20})
    plt.savefig('plot2.png')
    # plt.show()

    fig3 = plt.figure(figsize=(21,9), dpi=150, facecolor=None, edgecolor=None, frameon=False)
    plt.plot(df2['people_vaccinated'], label='People vaccinated with one dose')
    plt.plot(df2['people_fully_vaccinated'], label='People vaccinated with two doses')
    plt.plot(df2['projected_d1'], label='Projection')
    plt.title('India Vaccination Trend', loc='left', fontname=font_name, fontsize=40, fontweight='bold')
    plt.xlabel('Days', fontname=font_name, fontsize=28, fontweight='bold')
    plt.ylabel('Population', fontname=font_name, fontsize=28, fontweight='bold')
    plt.xticks(fontname=font_name, fontsize=8, rotation='vertical')
    plt.yticks(fontname=font_name, fontsize=20)
    plt.ticklabel_format(axis='y', style='plain', scilimits=None, useOffset=None)
    plt.annotate(f'Projected: {max_possible:,}', xy=('2021-08-20', 1000000000), fontname=font_name, fontsize=32)
    plt.annotate(f'@ {cvr:,} per day', xy=('2021-08-20', 930000000), fontname=font_name, fontsize=20)
    plt.annotate(f'{single_so_far:,}', xy=('2021-06-30', 220000000), fontname=font_name, fontsize=20)
    plt.annotate(f'{full_so_far:,}', xy=('2021-06-30', 50000000), fontname=font_name, fontsize=20)
    plt.tight_layout()
    # plt.legend(loc=9)
    plt.legend(loc=2, prop={'family':font_name, 'size':20})
    plt.savefig('plot3.png')
    # plt.show()

    plt.close()

if __name__ == '__main__':
    main()
