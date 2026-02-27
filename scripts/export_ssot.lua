local script_dir = arg[0]:match("(.*/)")
package.path = script_dir .. "?.lua;" .. script_dir .. "../data/ssot/?.lua;" .. package.path

local encode = require("json_encode")
local data = require("init")
print(encode(data))
