#!/bin/bash
# 1. Check if a port is in use
check_port() {
  local port=$1
  if lsof -i :$port > /dev/null; then
    echo "Port $port is in use"
  else
    echo "Port $port is free"
  fi
}

# 2. Count lines of code in a directory
count_lines() {
  local dir=${1:-.}
  find $dir -name '*.sh' -o -name '*.js' -o -name '*.py' | xargs wc -l
}

# 3. Generate a random password
generate_password() {
  local length=${1:-16}
  LC_ALL=C tr -dc 'A-Za-z0-9!@#$%^&*()_+' </dev/urandom | head -c $length
  echo
}

# 4. Convert timestamp to human-readable date
timestamp_to_date() {
  local timestamp=$1
  date -d @$timestamp
}

# 5. Find large files in a directory
find_large_files() {
  local dir=${1:-.}
  local size=${2:-"+100M"}
  find $dir -type f -size $size -exec ls -lh {} \; | awk '{ print $9 ": " $5 }'
}

# 6. Monitor CPU usage
monitor_cpu() {
  local duration=${1:-60}
  top -b -n $duration | grep "Cpu(s)" | awk '{print $2 + $4}'
}

# 7. Backup a directory
backup_dir() {
  local src=$1
  local dest=$2
  tar -czf $dest/backup_$(date +%Y%m%d_%H%M%S).tar.gz $src
}

# 8. Find and replace in files
find_replace() {
  local find=$1
  local replace=$2
  local dir=${3:-.}
  grep -rl "$find" $dir | xargs sed -i "s/$find/$replace/g"
}

# 9. Check disk usage
check_disk_usage() {
  df -h | awk '$NF=="/"{printf "Disk Usage: %d/%dGB (%s)\n", $3,$2,$5}'
}

# 10. Kill process by name
kill_process() {
  local name=$1
  pkill -f $name
}

# 11. List open ports
list_open_ports() {
  netstat -tuln | awk '/LISTEN/{print $4}' | cut -d: -f2 | sort -n | uniq
}

# 12. Check if a website is up
check_website() {
  local url=$1
  if curl -s --head $url | grep "200 OK" > /dev/null; then
    echo "$url is up"
  else
    echo "$url is down"
  fi
}

# 13. Extract various archive types
extract_archive() {
  local file=$1
  case $file in
    *.tar.bz2) tar xjf $file ;;
    *.tar.gz) tar xzf $file ;;
    *.bz2) bunzip2 $file ;;
    *.rar) unrar x $file ;;
    *.gz) gunzip $file ;;
    *.tar) tar xf $file ;;
    *.tbz2) tar xjf $file ;;
    *.tgz) tar xzf $file ;;
    *.zip) unzip $file ;;
    *.Z) uncompress $file ;;
    *) echo "'$file' cannot be extracted" ;;
  esac
}

# 14. Get public IP address
get_public_ip() {
  curl -s https://api.ipify.org
}

# 15. Monitor memory usage
monitor_memory() {
  free -m | awk 'NR==2{printf "Memory Usage: %s/%sMB (%.2f%%)\n", $3,$2,$3*100/$2 }'
}

# 16. Find duplicate files
find_duplicates() {
  local dir=${1:-.}
  find $dir -type f -print0 | xargs -0 md5sum | sort | uniq -w32 --all-repeated=separate
}

# 17. Batch rename files
batch_rename() {
  local pattern=$1
  local replacement=$2
  for file in *$pattern*; do
    mv "$file" "${file/$pattern/$replacement}"
  done
}

# 18. Check SSL certificate expiration
check_ssl_expiry() {
  local domain=$1
  echo | openssl s_client -servername $domain -connect $domain:443 2>/dev/null | openssl x509 -noout -dates
}

# 19. Convert image format
convert_image() {
  local input=$1
  local output=$2
  convert $input $output
}

# 20. Monitor network traffic
monitor_network() {
  local interface=${1:-eth0}
  local duration=${2:-60}
  iftop -i $interface -t -s $duration
}

# 21. Run Docker container
run_docker() {
  local image_name=$1
  local container_name=$2
  docker run -d --name $container_name $image_name
}

# 22. Create database backup
backup_database() {
  local db_name=$1
  local output_file=${2:-"backup_$(date +%Y%m%d_%H%M%S).sql"}
  pg_dump $db_name > $output_file
}

# 23. Run API tests
run_api_tests() {
  local api_url=$1
  pytest tests/api_tests.py --url $api_url
}

# 24. Analyze logs
analyze_logs() {
  local log_file=$1
  local pattern=$2
  awk -v pat="$pattern" '$0~pat{print $0}' $log_file | sort | uniq -c | sort -rn
}

# Example usage
echo "Checking if port 8080 is in use:"
check_port 8080

echo "Counting lines of code in current directory:"
count_lines

echo "Generating a random password:"
generate_password

echo "Converting timestamp to date:"
timestamp_to_date 1621234567

echo "Finding large files in current directory:"
find_large_files

echo "Checking disk usage:"
check_disk_usage

echo "Listing open ports:"
list_open_ports

echo "Checking if example.com is up:"
check_website https://example.com

echo "Getting public IP address:"
get_public_ip

echo "Monitoring memory usage:"
monitor_memory
