---@class Link
---@field href string
---@field text string

---@class InlineA
---@field a Link

---@class InlineB
---@field b string

---@class InlineStrong
---@field strong string

---@class InlineEm
---@field em string

---@alias Inline string | InlineA | InlineB | InlineStrong | InlineEm

---@alias PContent Inline | Inline[]

---@class BlockP
---@field p PContent
---@field class? string

---@class BlockUl
---@field ul PContent[]

---@class BlockH4
---@field h4 string

---@alias Block BlockP | BlockUl | BlockH4

---@alias Body Block[]

---@class WorkEntry
---@field start integer
---@field finish? integer
---@field role string
---@field org string
---@field org_url? string
---@field description string
---@field description_small? boolean

---@class EducationEntry
---@field start integer
---@field finish integer
---@field institution string
---@field degree string
---@field degree2? string
---@field degree2_note? string
---@field thesis? string
---@field courses? string

---@class Award
---@field year integer
---@field name string
---@field org string
---@field description string

---@class SiteNode
---@field id string
---@field title string
---@field body Body
---@field children? string[]

---@class Identity
---@field name { first: string, last: string }
---@field email string
---@field site string
---@field github string
---@field scholar string
---@field summary string
---@field languages string[]
---@field tools string[]
---@field hard_skills string[]
---@field soft_skills string[]
---@field interests string[]

---@class Career
---@field work WorkEntry[]
---@field education EducationEntry[]
---@field awards Award[]

---@class Site
---@field root string
---@field nodes SiteNode[]

local dsl = {}

---@param href string
---@param text string
---@return InlineA
function dsl.a(href, text)
  return { a = { href = href, text = text } }
end

---@param text string
---@return InlineB
function dsl.b(text)
  return { b = text }
end

---@param text string
---@return InlineStrong
function dsl.strong(text)
  return { strong = text }
end

---@param text string
---@return InlineEm
function dsl.em(text)
  return { em = text }
end

---@param content PContent
---@param class? string
---@return BlockP
function dsl.p(content, class)
  if class then
    return { p = content, class = class }
  end
  return { p = content }
end

---@param items PContent[]
---@return BlockUl
function dsl.ul(items)
  return { ul = items }
end

---@param text string
---@return BlockH4
function dsl.h4(text)
  return { h4 = text }
end

return dsl
