local encode

local function encode_string(s)
  s = s:gsub('\\', '\\\\'):gsub('"', '\\"'):gsub('\n', '\\n')
    :gsub('\r', '\\r'):gsub('\t', '\\t')
  return '"' .. s .. '"'
end

local function is_array(t)
  local i = 0
  for _ in pairs(t) do
    i = i + 1
    if t[i] == nil then return false end
  end
  return true
end

local function encode_array(t)
  local parts = {}
  for i = 1, #t do parts[i] = encode(t[i]) end
  return "[" .. table.concat(parts, ",") .. "]"
end

local function encode_map(t)
  local parts = {}
  for k, v in pairs(t) do
    parts[#parts + 1] = encode_string(tostring(k)) .. ":" .. encode(v)
  end
  return "{" .. table.concat(parts, ",") .. "}"
end

encode = function(val)
  local t = type(val)
  if val == nil then return "null"
  elseif t == "boolean" then return tostring(val)
  elseif t == "number" then return tostring(val)
  elseif t == "string" then return encode_string(val)
  elseif t == "table" then
    if is_array(val) then return encode_array(val) end
    return encode_map(val)
  else
    error("unsupported type: " .. t)
  end
end

return encode
