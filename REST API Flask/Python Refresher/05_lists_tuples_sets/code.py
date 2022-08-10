l = ["Bob", "Rolf", "Anne"]
t = ("Bob", "Rolf", "Anne")
s = {"Bob", "Rolf", "Anne"}

#TODO: Access individual items in lists and tuples using the index.

print(l[0])
print(t[0])
#TODO: print(s[0])  # This gives an error because sets are unordered, so accessing element 0 of something without order doesn't make sense.

#TODO: Modify individual items in lists using the index.

l[0] = "Smith"
#TODO: t[0] = "Smith"  # This gives an error because tuples are "immutable".

print(l)
print(t)

#TODO: Add to a list by using `.append`

l.append("Jen")
print(l)
#TODO: Tuples cannot be appended to because they are immutable.

#TODO: Add to sets by using `.add`

s.add("Jen")
print(s)

#TODO: Sets can't have the same element twice.

s.add("Bob")
print(s)
