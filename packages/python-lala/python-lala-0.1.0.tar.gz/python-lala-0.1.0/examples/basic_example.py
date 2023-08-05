import os
import lala

# LOAD ALL RECORDS TO ANALYSE AND AVAILABLE PRIMERS
with open(os.path.join('data', 'example_logs.txt'), 'r') as f:
    entries, errored_lines = lala.logs_lines_to_dataframe(f)

# PLOT COUNTRIES PIE CHART
ax, country_values = lala.plot_piechart(entries, 'country_name')
ax.figure.set_size_inches((5, 5))
ax.figure.savefig('basic_example_piechart.png', bbox_inches='tight')

# PLOT COUNTRIES MAP
ax = lala.countries_colormap(country_values.iteritems(), figsize=(12, 8))
lala.plot_geo_positions(entries, ax)
ax.figure.savefig('basic_example_worldmap.png', bbox_inches='tight')

# PLOT UK CONNECTIONS TIMELINE
uk_entries = entries[entries.country_name == 'United Kingdom']
ax = lala.plot_entries_in_time(uk_entries, bins_per_day=2)
ax.figure.savefig('basic_example_timeline.png', bbox_inches='tight')
