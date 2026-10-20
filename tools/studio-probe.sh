#!/usr/bin/env bash
# Run ON the Mac Studio (copy over, or ssh in once Remote Login is on). Prints what the local lane can carry.
# Paste the output into notes/log.md. Then follow docs/MODEL-ROUTING.md section 3 for the tier it names.
set -u
echo "host:   $(hostname)  macOS $(sw_vers -productVersion)"
echo "chip:   $(sysctl -n machdep.cpu.brand_string)"
mem_gb=$(( $(sysctl -n hw.memsize) / 1024 / 1024 / 1024 ))
echo "memory: ${mem_gb} GB   (unified; LM Studio's default GPU budget is about 75% of it)"
echo "disk:   $(df -h / | awk 'NR==2{print $4" free"}')"
echo "remote login: $(sudo -n systemsetup -getremotelogin 2>/dev/null || echo 'unknown (needs sudo); check System Settings > General > Sharing')"
for app in "LM Studio" Ollama Zoom Discord; do [ -d "/Applications/$app.app" ] && echo "app:    $app present" || echo "app:    $app missing"; done
for t in lms ollama ffmpeg yt-dlp brew python3; do printf "tool:   %-8s %s\n" "$t" "$(command -v $t 2>/dev/null || echo -)"; done
echo "lm studio models: $(du -sh ~/.lmstudio/models 2>/dev/null | cut -f1 || echo none)"
ls ~/.lmstudio/models/*/ 2>/dev/null | sed 's/^/   /'
echo "server :1234 -> $(curl -s --max-time 2 localhost:1234/v1/models | head -c 300 || echo 'not running')"
echo "server :11434 -> $(curl -s --max-time 2 localhost:11434/api/tags | head -c 300 || echo 'not running')"
echo
if   [ "$mem_gb" -ge 160 ]; then echo "tier:   XL  (192 GB+): Qwen3-235B-A22B 4-bit or gpt-oss-120b as the workhorse, Qwen3-VL-32B for slides"
elif [ "$mem_gb" -ge 90  ]; then echo "tier:   L   (96 to 128 GB): gpt-oss-120b workhorse, Qwen3-30B-A3B for bulk labels, Qwen3-VL-8B for slides"
elif [ "$mem_gb" -ge 60  ]; then echo "tier:   M   (64 GB): Qwen3-30B-A3B workhorse (about 17 GB), Qwen3-32B dense for the judge sample, Qwen3-VL-8B for slides"
else                              echo "tier:   S   (32 to 36 GB): Qwen3-30B-A3B 4-bit workhorse, gpt-oss-20b alternate, Qwen3-VL-8B for slides"; fi
echo "names are LM Studio's as of Oct 2026; take the newest instruct MoE that fits in 60% of RAM if these have moved on"
