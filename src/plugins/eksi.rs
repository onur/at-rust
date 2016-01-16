

use at::{AtRust, AtTrigger};
use plugins::get;

use select::document::Document;
use select::predicate::{Attr, Class, Name};
use rand::Rng;
use rand;



pub fn eksi(trigger: &AtTrigger, at: &AtRust) {
    let url = format!("https://eksisozluk.com/{}", trigger.command_message);
    let body = get(&url[..]);

    let body_str = body.unwrap();
    let document = Document::from_str(&body_str[..]);

    let mut entries: Vec<String> = Vec::new();

    for entry in document.find(Attr("id", "entry-list")).find(Name("li")).iter() {
        let entry_text = entry.find(Class("content")).first().unwrap().text();
        // FIXME: Do I really need to clone text?
        entries.push(entry_text.clone());
    }

    let mut rng = rand::thread_rng();

    at.reply(trigger, &entries[rng.gen::<usize>() % entries.len()][..]);
}
