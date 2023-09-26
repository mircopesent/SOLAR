clear all
close all
clc


%% Import data
months=[31 28 31 30 31 30 31 31 30 31 30 31];
counter=0;
for i=1:length(months)
    for j=1:months(i)
        counter=counter+1;
        file_name="data\data"+num2str(i,'%02.f')+num2str(j,'%02.f')+".csv";
        data=readtable(file_name);
        data_array=table2array(data);
        total_irrad(counter)=sum(data_array(:,2).*data_array(:,3));
        clear data
        clear data_array
    end
end

%% Plot data

XDates = [datetime(2014,1,1:31) datetime(2014,2,1:28) datetime(2014,3,1:31) datetime(2014,4,1:30) datetime(2014,5,1:31) datetime(2014,6,1:30) datetime(2014,7,1:31) datetime(2014,8,1:31) datetime(2014,9,1:30) datetime(2014,10,1:31) datetime(2014,11,1:30) datetime(2014,12,1:31)];

figure(1)
hold on
plot(XDates,total_irrad/1e12,'LineWidth',2)
xlabel("Date",'FontSize',14)
ylabel("Total irradiance [GW]",'FontSize',14)
title("Total solar irradiance in Switzerland",'FontSize',20)
hold off