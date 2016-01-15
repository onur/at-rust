

use std::io::{BufReader, BufWriter};
use std::boxed::Box;

use irc::client::prelude::*;
use irc::client::conn::NetStream;
use regex::Regex;


pub trait AtHandler {
    fn handle(&self, msg: &AtTrigger, at: &AtRust);
}


impl<F> AtHandler for F where F: Fn(&AtTrigger, &AtRust)
{
    fn handle(&self, msg: &AtTrigger, at: &AtRust) {
        (*self)(msg, at);
    }
}


struct AtPlugin {
    regex: &'static str,
    handler: Box<AtHandler>,
}


impl AtPlugin {
    fn handle(&self, msg: &AtTrigger, at: &AtRust) {
        let m = self.handler.as_ref();
        m.handle(msg, at);
    }
}


pub struct AtTrigger {
    pub user: String,
    pub command: String,
    pub command_message: String,
    pub message: String,
    pub target: String,
}


impl AtTrigger {
    pub fn new(message: &Message) -> Option<AtTrigger> {

        // Message type from irc crate
        // PREFIX Some("onur!~onur@localhost")
        // COMMAND PRIVMSG
        // ARGS ["#onur"]
        // SUFFIX Some("hello")

        if !message.command.eq("PRIVMSG") {
            return None;
        }

        // split nickname
        let mut split = message.prefix.as_ref().unwrap().split("!");
        let user = split.nth(0).unwrap();

        // command is just first word
        let mut command_vec: Vec<&str> = message.suffix.as_ref().unwrap().split(' ').collect();
        let command = command_vec.remove(0);
        let command_message = command_vec.join(" ");

        Some(AtTrigger {
            user: user.to_owned(),
            command: command.to_owned(),
            command_message: command_message.to_owned(),
            message: message.suffix.as_ref().unwrap().to_owned(),
            target: message.args[0].to_owned(),
        })

    }
}



pub struct AtRust {
    pub server: IrcServer<BufReader<NetStream>, BufWriter<NetStream>>,
    handlers: Vec<AtPlugin>,
}


impl AtRust {
    pub fn from_config(config: Config) -> AtRust {
        AtRust {
            server: IrcServer::from_config(config).unwrap(),
            handlers: Vec::new(),
        }
    }

    /// Connect irc server and stay there forever
    pub fn connect(&self) {

        self.server.identify().unwrap();

        loop {
            self.message_loop();

            // reconnect if we get disconnected
            self.server.reconnect().unwrap();
            self.server.identify().unwrap();
        }
    }

    fn message_loop(&self) {

        for message in self.server.iter() {
            let message = message.unwrap();

            // PRIVMSG handlers
            if &message.command[..] == "PRIVMSG" {

                match AtTrigger::new(&message) {
                    Some(msg) => self.run_privmsg_handlers(msg),
                    _ => {}
                }

            }
        }

    }

    fn run_privmsg_handlers(&self, msg: AtTrigger) {

        // TODO: Use closures here
        for handler in &self.handlers {
            match Regex::new(handler.regex) {
                Ok(re) => {
                    if re.is_match(&msg.command) {
                        handler.handle(&msg, &self);
                    }
                }
                Err(_) => println!("THERE WAS A FUCKING ERROR ON REGEX: {}", handler.regex),
            }
        }
    }

    pub fn say(&self, trigger: &AtTrigger, src: &str) {
        self.server.send_privmsg(&trigger.target[..], src).unwrap();
    }

    pub fn reply(&self, trigger: &AtTrigger, src: &'static str) {
        let message = format!("{}: {}", trigger.user, src);
        self.say(trigger, &message[..]);
    }

    pub fn register_handler<P: 'static>(&mut self, regex: &'static str, p: P)
        where P: AtHandler
    {

        self.handlers.push(AtPlugin {
            regex: regex,
            handler: Box::new(p),
        });

    }
}
