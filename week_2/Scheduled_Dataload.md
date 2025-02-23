Tutorial link 
https://youtu.be/_-li_z97zog?si=G6jZbkfJb3GAyqrd

This section is very similar to the previous one described in Load_Taxi_Data.md. We're doing very similar stuff, just in two differnt scenarios

1. Using a scheduler to trigger at cedrtain times
2. Filling in past data 

The kestra file for this section is 02_postgres_taxi_scheduled.yaml

Let look at the differences. 

1. Inputs

We don't need to input the month, just whether we're interested in the green or yellow dataset and that will come from the trigger ( see below )

2. Triggers

At the bottom of the file you will find the following cron job definitions

```
triggers:
  - id: green_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 9 1 * *"
    inputs:
      taxi: green

  - id: yellow_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 10 1 * *"
    inputs:
      taxi: yellow
````

You can use https://crontab.guru/ to see what the regular expressions mean and generate new ones. 

This triggers are for future events, now to backfil we will use the Kestra interface. 

Import the flow into Kestra as before. 
Select the flow and go to the triggers tab. There you will see the 2 triggers that are defined in the file. 

Each trigger has a convenient option to backfill executions, all you have to do is select a start and end date and the taxi type. 

