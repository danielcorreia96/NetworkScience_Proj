echo "calculating frequency by user"
sh freq_user.sh
echo "calculating number of tweets per day"
sh freq_by_day.sh
echo "drawing tweets per month"
sh draw_montlhy_graphs.sh
echo "drawing tweets for random users"
sh draw_user_profile.sh