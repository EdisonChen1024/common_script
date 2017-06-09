local math = math
local os = os
local string = string
local ONE_DAY = 86400
local SINGLE = 1
local DOUBLE = 2
local config = {
	now   = DOUBLE,
	year  = 2017,
	month = 4,
	day   = 6,
	type  = SINGLE,
}
local fd, err = io.open("fuck.log", "w")
assert(fd, err)

-- [1, 7] : [星期一, 星期日]
local function get_wday(time)
	local date = os.date("*t", time)
	local wday = date.wday
	if wday == 1 then
		return 7
	else
		return wday - 1
	end
end

local function get_date(time)
	local date = os.date("*t", time)
	-- print(string.format("%04d年%02d月%02d日 %02d时%02d分%02d秒", date.year, date.month, date.day, date.hour, date.min, date.sec))
	return string.format("%04d年%02d月%02d日", date.year, date.month, date.day)
end

local function get_now_type()
	if config.now then
		return config.now
	end

	local now_timestamp = os.time()
	local date = os.date("*t", now_timestamp)
	assert(config.year)
	assert(config.month)
	assert(config.day)
	assert(config.type)
	date.year  = config.year
	date.month = config.month
	date.day   = config.day
	local config_timestamp = os.time(date)
	local now_week = now_timestamp / (ONE_DAY * 7)
	local config_week = config_timestamp / (ONE_DAY * 7)
end

local function print_week_range(time, t)
	time = time or os.time()
	local s = ""
	if t == SINGLE then
		s = "单"
	elseif t == DOUBLE then
		s = "双"
	end
	local wday = get_wday(time)
	local start_time = time - (wday - 1) * ONE_DAY
	local end_time = time + (7 - wday) * ONE_DAY
	local line = string.format("%s-%s %s\n", get_date(start_time), get_date(end_time), s)
	fd:write(line)
--~ 	print(string.format("%s-%s %s", get_date(start_time), get_date(end_time), s))
end

local function print_schedule(amount)
	local now = os.time()
	local t = get_now_type()
	for i = 1, amount do
		print_week_range(now + ONE_DAY * 7 * (i - 1), t)
		t = t + 1
		if t > DOUBLE then
			t = SINGLE
		end
	end
end

print_schedule(520)
fd:close()
