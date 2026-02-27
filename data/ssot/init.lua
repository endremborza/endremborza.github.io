package.path = arg[0]:match("(.*/)")  .. "?.lua;" .. package.path

return {
  identity = require("identity"),
  career = require("career"),
  site = require("site"),
}
