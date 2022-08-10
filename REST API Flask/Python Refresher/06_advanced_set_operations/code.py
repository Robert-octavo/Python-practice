#TODO: -- Difference between two sets --

friends = {"Bob", "Rolf", "Anne"}
abroad = {"Bob", "Anne"}

#TODO: local_friends = ...
#TODO: If there are 3 friends, and 2 are abroad, that means that 1 friend is local.
#TODO: We can easily calculate which names are in `friends` but not in `abroad` by using `.difference`

local = friends.difference(abroad)
print(local)

print(abroad.difference(friends))  # This returns an empty set

#TODO: -- Union of two sets --

local = {"Rolf"}
abroad = {"Bob", "Anne"}

#TODO: friends = ...
#TODO: If we have 1 local friend and 2 abroad friends, we could calculate the total friends by using `.union`

friends = local.union(abroad)
print(friends)

#TODO: -- Intersection of two sets --

art = {"Bob", "Jen", "Rolf", "Charlie"}
science = {"Bob", "Jen", "Adam", "Anne"}

#TODO:Given these two sets of students, we can calculate those who do both art and science by using `.intersection`

both = art.intersection(science)
print(both)
