import twint
import nest_asyncio

nest_asyncio.apply()
c = twint.Config()
c.Username = "brendan_webdev"
c.Followers = True
c.Resume = "resume.txt"
c.Output = "testing.csv"
twint.run.Following(c)